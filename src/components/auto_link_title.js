import React from "react";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import linkMetadata from "../generated/link-metadata.json";

const isExternalUrl = (value) => /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(value || "");

const joinWithBaseUrl = (baseUrl, value) => {
	const normalizedBase = baseUrl.endsWith("/") ? baseUrl : `${baseUrl}/`;
	const normalizedValue = (value || "").replace(/^\//, "");
	return `${normalizedBase}${normalizedValue}`;
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

const AutoLinkTitle = ({ url = "/" }) => {
	const { siteConfig } = useDocusaurusContext();
	const baseUrl = siteConfig?.baseUrl || "/";
	const normalizedUrl = normalizeRoutePath(url);
	const metadata =
		linkMetadata[url] || (normalizedUrl ? linkMetadata[normalizedUrl] : null);
	const title = metadata?.title || url;
	const resolvedHref = isExternalUrl(url) ? url : joinWithBaseUrl(baseUrl, url);

	return (
		<Link
			href={resolvedHref}
			target={isExternalUrl(url) ? "_blank" : undefined}
			rel={isExternalUrl(url) ? "noopener noreferrer" : undefined}
		>
			{title}
		</Link>
	);
};

export default AutoLinkTitle;
