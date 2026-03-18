import React from "react";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import styles from "./link_card.module.css";
import linkMetadata from "../generated/link-metadata.json";

const isExternalUrl = (href) =>
	/^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(href || "");

const joinWithBaseUrl = (baseUrl, value) => {
	const normalizedBase = baseUrl.endsWith("/") ? baseUrl : `${baseUrl}/`;
	const normalizedValue = (value || "").replace(/^\//, "");
	return `${normalizedBase}${normalizedValue}`;
};

const normalizeSiteName = (href, siteName) => {
	if (siteName) {
		return siteName;
	}

	if (!href) {
		return "";
	}

	if (!isExternalUrl(href)) {
		return "reincarnation_tech";
	}

	try {
		return new URL(href).hostname.replace(/^www\./i, "");
	} catch {
		return href;
	}
};

const LinkCard = ({ href = "/", title, description, image, siteName, alt }) => {
	const { siteConfig } = useDocusaurusContext();
	const baseUrl = siteConfig?.baseUrl || "/";
	const metadata = linkMetadata[href] || {};
	const cardTitle = title || metadata.title || href;
	const cardDescription = description || metadata.description || "";
	const cardImage = image || metadata.image || null;
	const isIconImage = !image && metadata.imageType === "icon";
	const cardSiteName = normalizeSiteName(href, siteName || metadata.siteName);
	const resolvedHref = isExternalUrl(href) ? href : joinWithBaseUrl(baseUrl, href);
	const resolvedImage = cardImage
		? isExternalUrl(cardImage)
			? cardImage
			: joinWithBaseUrl(baseUrl, cardImage)
		: null;

	return (
		<Link
			className={styles.linkCard}
			href={resolvedHref}
			target={isExternalUrl(href) ? "_blank" : undefined}
			rel={isExternalUrl(href) ? "noopener noreferrer" : undefined}
		>
			<div className={styles.thumb}>
				{resolvedImage ? (
					<img
						className={isIconImage ? styles.iconImage : styles.image}
						src={resolvedImage}
						alt={alt || cardTitle}
						loading="lazy"
					/>
				) : (
					<div className={styles.placeholder}>LINK</div>
				)}
			</div>
			<div className={styles.body}>
				<div className={styles.title}>{cardTitle}</div>
				{cardDescription ? (
					<div className={styles.description}>{cardDescription}</div>
				) : null}
				{cardSiteName ? (
					<div className={styles.site}>{cardSiteName}</div>
				) : null}
			</div>
		</Link>
	);
};

export default LinkCard;
