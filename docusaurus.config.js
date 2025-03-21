// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

// const lightCodeTheme = require("prism-react-renderer/themes/github");
// const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
	title: "Reincarnation+#Tech",
	tagline: "Dinosaurs are cool",
	favicon: "img/favicon.ico",
	staticDirectories: ["public", "static"],

	projectName: "fereria.github.io",
	organizationName: "reincarnation_tech",
	trailingSlash: false,

	// Set the production url of your site here
	url: "https://fereria.github.io",
	// Set the /<baseUrl>/ pathname under which your site is served
	// For GitHub pages deployment, it is often '/<projectName>/'
	baseUrl: "/reincarnation_tech/",

	onBrokenLinks: "throw",
	onBrokenMarkdownLinks: "warn",

	// Even if you don't use internalization, you can use this field to set useful
	// metadata like html lang. For example, if your site is Chinese, you may want
	// to replace "en" with "zh-Hans".
	plugins: [require.resolve("docusaurus-plugin-image-zoom")],
	presets: [
		[
			"classic",
			/** @type {import('@docusaurus/preset-classic').Options} */
			({
				docs: {
					routeBasePath: "/",
					sidebarPath: require.resolve("./sidebars.js"),
					// Please change this to your repo.
					// Remove this to remove the "edit this page" links.
					showLastUpdateTime: true, // この行を追加
					showLastUpdateAuthor: true, // お好みでこちらも
				},
				blog: {
					showReadingTime: true,
					// Please change this to your repo.
					// Remove this to remove the "edit this page" links.
				},
				theme: {
					customCss: require.resolve("./src/css/custom.css"),
				},
			}),
		],
	],
	i18n: {
		defaultLocale: "ja",
		locales: ["ja"],
	},
	themeConfig: {
		// Replace with your project's social card
		zoom: {
			selector: ".markdown :not(em) > img",
			config: {
				// options you can specify via https://github.com/francoischalifour/medium-zoom#usage
				background: {
					light: "rgb(255, 255, 255)",
					dark: "rgb(50, 50, 50)",
				},
			},
		},
		image: "img/docusaurus-social-card.jpg",
		metadata: [{ name: "twitter:card", content: "summary" }],
		algolia: {
			apiKey: "a348c5e70a7f17978dd23130e9d1483c",
			indexName: "reincarnation-tech",
			appId: "88RL2KSSCA",
		},
		navbar: {
			title: "Reincarnation+#Tech",
			logo: {
				alt: "My Site Logo",
				src: "img/logo.svg",
			},
			// Tab を追加する場合はここに追加
			items: [
				{ to: "/blog", label: "Blog", position: "left" },
				{
					to: "/dcc",
					sidebarId: "dccSidebar",
					position: "left",
					label: "DCCTool",
				},
				{
					to: "/pipeline",
					label: "Pipeline",
					sidebarId: "pipelineSidebar",
					position: "left",
				},
				{
					to: "/pg",
					sidebarId: "programmingSidebar",
					position: "left",
					label: "Programming",
				},
				{
					to: "/game_engine",
					sidebarId: "gameEngineSidebar",
					position: "left",
					label: "GameEngine",
				},
				{
					to: "/ta",
					sidebarId: "taSidebar",
					position: "left",
					label: "TechArtist",
				},
				{
					to: "/tags",
					label: "Tags",
					position: "left",
				},
				{
					href: "https://github.com/fereria/reincarnation_tech",
					label: "GitHub",
					position: "right",
				},
			],
		},
		footer: {
			style: "dark",
			links: [
				{
					title: "SocialMedia",
					items: [
						{
							label: "Twitter",
							href: "https://twitter.com/fereria",
						},
						{
							label: "Reincarnation+#Tech",
							href: "https://fereria.github.io/reincarnation_tech/",
						},
						{
							label: "GitHub",
							href: "https://github.com/fereria/reincarnation_tech",
						},
					],
				},
				{
					title: "Link",
					items: [
						{
							label: "Docusaurus",
							href: "https://docusaurus.io/",
						},
						{
							label: "React",
							href: "https://ja.react.dev/",
						},
					],
				},
			],
			copyright: `Copyright © ${new Date().getFullYear()} Reincarnation#Tech, Built with Megumi Ando.`,
		},
		// prism: {
		// 	theme: lightCodeTheme,
		// 	darkTheme: darkCodeTheme,
		// },
	},
};

module.exports = config;
