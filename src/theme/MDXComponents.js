import MDXComponents from "@theme-original/MDXComponents";
import AutoLinkTitle from "@site/src/components/auto_link_title.js";
import CodePen from "@site/src/components/codepen.js";
import Marker from "@site/src/components/marker.js";
import { TwitterTweetEmbed } from "react-twitter-embed";
import ReactEmbedGist from "react-embed-gist";

export default {
	// Re-use the default mapping
	...MDXComponents,
	AutoLinkTitle,
	ReactEmbedGist,
	TwitterTweetEmbed,
	CodePen,
	Marker,
};
