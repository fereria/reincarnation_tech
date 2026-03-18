const fs = require("fs");
const path = require("path");

const ROOT_DIR = path.resolve(__dirname, "..");
const OUTPUT_FILE = path.join(
	ROOT_DIR,
	"src",
	"generated",
	"link-metadata.json"
);
const SITE_ORIGIN = "https://fereria.github.io";
const BASE_URL = "/reincarnation_tech";
const CONTENT_DIRS = [
	path.join(ROOT_DIR, "docs"),
	path.join(ROOT_DIR, "blog"),
	path.join(ROOT_DIR, "src", "pages"),
];
const CONTENT_EXTENSIONS = new Set([".md", ".mdx"]);
const LINK_CARD_PATTERN = /<LinkCard\b[\s\S]*?\bhref=(["'])(.*?)\1[\s\S]*?\/>/g;
const EXCERPT_LIMIT = 160;
const HTTP_URL_PATTERN = /^https?:\/\//i;
const EXTERNAL_SCHEME_PATTERN = /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i;

const stripMarkdown = (value) =>
	value
		.replace(/```[\s\S]*?```/g, " ")
		.replace(/`[^`]*`/g, " ")
		.replace(/!\[[^\]]*]\([^)]*\)/g, " ")
		.replace(/\[[^\]]*]\([^)]*\)/g, " ")
		.replace(/<[^>]+>/g, " ")
		.replace(/[#>*_~|-]/g, " ")
		.replace(/\s+/g, " ")
		.trim();

const createExcerpt = (body) => {
	const plain = stripMarkdown(body);
	if (!plain) {
		return "";
	}

	return plain.length > EXCERPT_LIMIT
		? `${plain.slice(0, EXCERPT_LIMIT - 3).trim()}...`
		: plain;
};

const walkFiles = (dirPath) => {
	if (!fs.existsSync(dirPath)) {
		return [];
	}

	const entries = fs.readdirSync(dirPath, { withFileTypes: true });
	return entries.flatMap((entry) => {
		const fullPath = path.join(dirPath, entry.name);
		if (entry.isDirectory()) {
			return walkFiles(fullPath);
		}
		return CONTENT_EXTENSIONS.has(path.extname(entry.name)) ? [fullPath] : [];
	});
};

const parseFrontMatter = (source) => {
	const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
	if (!match) {
		return { attributes: {}, body: source };
	}

	const attributes = {};
	for (const line of match[1].split(/\r?\n/)) {
		const item = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
		if (!item) {
			continue;
		}
		attributes[item[1]] = item[2].trim().replace(/^['"]|['"]$/g, "");
	}

	return {
		attributes,
		body: source.slice(match[0].length),
	};
};

const normalizeRoutePath = (value) => {
	if (!value) {
		return null;
	}

	let normalized = value.trim();
	if (!normalized.startsWith("/")) {
		normalized = `/${normalized}`;
	}
	if (normalized.length > 1) {
		normalized = normalized.replace(/\/+$/, "");
	}
	return normalized;
};

const toDocRoute = (filePath, attributes) => {
	const relativePath = path.relative(ROOT_DIR, filePath).replace(/\\/g, "/");
	const parsed = path.parse(relativePath);

	if (attributes.slug) {
		return normalizeRoutePath(attributes.slug);
	}

	if (relativePath.startsWith("docs/")) {
		const withoutPrefix = relativePath.replace(/^docs\//, "");
		const route = withoutPrefix.replace(path.extname(withoutPrefix), "");
		return normalizeRoutePath(route.replace(/\/index$/, ""));
	}

	if (relativePath.startsWith("blog/")) {
		const route = parsed.name === "index" ? parsed.dir : `${parsed.dir}/${parsed.name}`;
		return normalizeRoutePath(`/${route}`);
	}

	if (relativePath.startsWith("src/pages/")) {
		const route = relativePath
			.replace(/^src\/pages/, "")
			.replace(path.extname(relativePath), "")
			.replace(/\/index$/, "");
		return normalizeRoutePath(route || "/");
	}

	return null;
};

const collectInternalMetadata = () => {
	const metadata = new Map();

	for (const dirPath of CONTENT_DIRS) {
		for (const filePath of walkFiles(dirPath)) {
			const source = fs.readFileSync(filePath, "utf8");
			const { attributes, body } = parseFrontMatter(source);
			const route = toDocRoute(filePath, attributes);
			if (!route) {
				continue;
			}

			metadata.set(route, {
				href: route,
				title: attributes.title || path.parse(filePath).name,
				description:
					attributes.description || attributes.summary || createExcerpt(body),
				siteName: "reincarnation_tech",
				image: null,
				imageType: null,
			});
		}
	}

	return metadata;
};

const extractLinkCardHrefs = () => {
	const hrefs = new Set();

	for (const dirPath of CONTENT_DIRS) {
		for (const filePath of walkFiles(dirPath)) {
			const source = fs.readFileSync(filePath, "utf8");
			for (const match of source.matchAll(LINK_CARD_PATTERN)) {
				hrefs.add(match[2].trim());
			}
		}
	}

	return [...hrefs];
};

const decodeHtml = (value) =>
	value
		.replace(/&amp;/g, "&")
		.replace(/&lt;/g, "<")
		.replace(/&gt;/g, ">")
		.replace(/&quot;/g, '"')
		.replace(/&#39;/g, "'");

const findMetaContent = (html, key, attribute = "property") => {
	const escapedKey = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
	const pattern = new RegExp(
		`<meta[^>]+${attribute}=["']${escapedKey}["'][^>]+content=["']([^"']+)["'][^>]*>`,
		"i"
	);
	const reversePattern = new RegExp(
		`<meta[^>]+content=["']([^"']+)["'][^>]+${attribute}=["']${escapedKey}["'][^>]*>`,
		"i"
	);

	return decodeHtml(
		html.match(pattern)?.[1] || html.match(reversePattern)?.[1] || ""
	);
};

const findTitle = (html) => {
	const ogTitle = findMetaContent(html, "og:title");
	if (ogTitle) {
		return ogTitle;
	}

	const twitterTitle = findMetaContent(html, "twitter:title", "name");
	if (twitterTitle) {
		return twitterTitle;
	}

	const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
	return decodeHtml(titleMatch?.[1]?.replace(/\s+/g, " ").trim() || "");
};

const findDescription = (html) =>
	findMetaContent(html, "og:description") ||
	findMetaContent(html, "twitter:description", "name") ||
	findMetaContent(html, "description", "name");

const findImage = (html) =>
	findMetaContent(html, "og:image") ||
	findMetaContent(html, "twitter:image", "name");

const findIcon = (html) => {
	const iconPattern =
		/<link[^>]+rel=["']([^"']*\bicon\b[^"']*)["'][^>]+href=["']([^"']+)["'][^>]*>/gi;
	const reverseIconPattern =
		/<link[^>]+href=["']([^"']+)["'][^>]+rel=["']([^"']*\bicon\b[^"']*)["'][^>]*>/gi;

	for (const match of html.matchAll(iconPattern)) {
		if (match[2]) {
			return decodeHtml(match[2]);
		}
	}

	for (const match of html.matchAll(reverseIconPattern)) {
		if (match[1]) {
			return decodeHtml(match[1]);
		}
	}

	return null;
};

const absolutizeUrl = (value, baseUrl) => {
	if (!value) {
		return null;
	}

	try {
		return new URL(value, baseUrl).toString();
	} catch {
		return value;
	}
};

const createTitleFromHref = (href) => {
	try {
		const url = new URL(href);
		const segments = url.pathname
			.split("/")
			.filter(Boolean)
			.map((segment) => decodeURIComponent(segment));
		if (segments.length === 0) {
			return url.hostname;
		}
		if (url.hostname.includes("github.com") && segments.length >= 2) {
			return `${segments[0]}/${segments[1]}`;
		}
		return segments.slice(-2).join(" / ");
	} catch {
		return href;
	}
};

const buildFallbackMetadata = (href, siteName) => {
	let fallbackImage = null;
	let imageType = null;
	if (HTTP_URL_PATTERN.test(href)) {
		try {
			const url = new URL(href);
			fallbackImage = `${url.origin}/favicon.ico`;
			imageType = "icon";
		} catch {}
	}

	return {
		href,
		title: createTitleFromHref(href),
		description: "",
		image: fallbackImage,
		imageType,
		siteName,
	};
};

const fetchExternalMetadata = async (href) => {
	const controller = new AbortController();
	const timeoutId = setTimeout(() => controller.abort(), 8000);

	try {
		const response = await fetch(href, {
			headers: {
				"user-agent": "reincarnation-tech-link-card-bot/1.0",
			},
			signal: controller.signal,
		});
		const html = await response.text();
		const url = response.url || href;
		const previewImage = findImage(html);
		const iconImage = findIcon(html) || "/favicon.ico";

		return {
			href,
			title: findTitle(html) || href,
			description: findDescription(html),
			image: absolutizeUrl(previewImage || iconImage, url),
			imageType: previewImage ? "preview" : "icon",
			siteName:
				findMetaContent(html, "og:site_name") ||
				new URL(url).hostname.replace(/^www\./i, ""),
		};
	} catch (error) {
		return {
			...buildFallbackMetadata(
				href,
				new URL(href).hostname.replace(/^www\./i, "")
			),
			error: error.message,
		};
	} finally {
		clearTimeout(timeoutId);
	}
};

const createInternalAssetUrl = (value) => {
	if (!value) {
		return null;
	}

	try {
		return new URL(`${BASE_URL}${value.replace(/^\//, "")}`, SITE_ORIGIN).toString();
	} catch {
		return value;
	}
};

const main = async () => {
	const internalMetadata = collectInternalMetadata();
	const hrefs = extractLinkCardHrefs();
	const output = {};

	for (const href of hrefs) {
		const normalizedHref = normalizeRoutePath(href) || href;

		if (HTTP_URL_PATTERN.test(href)) {
			output[href] = await fetchExternalMetadata(href);
			continue;
		}

		if (EXTERNAL_SCHEME_PATTERN.test(href)) {
			output[href] = buildFallbackMetadata(href, href.split(":")[0] || href);
			continue;
		}

		const metadata = internalMetadata.get(normalizedHref);
		if (!metadata) {
			output[href] = buildFallbackMetadata(href, "reincarnation_tech");
			continue;
		}

		output[href] = {
			...metadata,
			image: createInternalAssetUrl(metadata.image),
		};
	}

	fs.mkdirSync(path.dirname(OUTPUT_FILE), { recursive: true });
	fs.writeFileSync(OUTPUT_FILE, `${JSON.stringify(output, null, 2)}\n`, "utf8");
	console.log(
		`Generated link metadata for ${Object.keys(output).length} LinkCard entr${
			Object.keys(output).length === 1 ? "y" : "ies"
		}.`
	);
};

main().catch((error) => {
	console.error(error);
	process.exitCode = 1;
});
