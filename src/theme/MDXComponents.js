import React from "react";
import MDXComponents from "@theme-original/MDXComponents";
import ExpandLink from "@site/src/components/expand_link.js";
import CodePen from "@site/src/components/codepen.js";
import { TwitterTweetEmbed } from "react-twitter-embed";
import Gist from "react-gist";

export default {
	// Re-use the default mapping
	...MDXComponents,
	ExpandLink,
	Gist,
	TwitterTweetEmbed,
	CodePen,
};
