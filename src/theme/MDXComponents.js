import React from "react";
import MDXComponents from "@theme-original/MDXComponents";
import AutoLinkTitle from "@site/src/components/auto_link_title.js";
import CodePen from "@site/src/components/codepen.js";
import Marker from "@site/src/components/marker.js";

import { TwitterTweetEmbed } from "react-twitter-embed";
import Gist from "react-gist";

export default {
	// Re-use the default mapping
	...MDXComponents,
	AutoLinkTitle,
	Gist,
	TwitterTweetEmbed,
	CodePen,
	Marker,
};
