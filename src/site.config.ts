import type { SiteConfig } from "@/types";

export const siteConfig: SiteConfig = {
	// Used as both a meta property (src/components/BaseHead.astro L:31 + L:49) & the generated satori png (src/pages/og-image/[slug].png.ts)
	author: "Chojan Shang",
	// Meta property used to construct the meta title property, found in src/components/BaseHead.astro L:11
	title: "Data Is Dead, Long Live Value.",
	// Meta property used as the default description meta property
	description:
		"Passionate about open source. Stay curious about knowledge. Build large-scale systems. Live alongside data.",
	// HTML lang property, found in src/layouts/Base.astro L:18
	lang: "en-GB",
	// Meta property, found in src/components/BaseHead.astro L:42
	ogLocale: "en_GB",
	// Date.prototype.toLocaleDateString() parameters, found in src/utils/date.ts.
	date: {
		locale: "en-GB",
		options: {
			day: "numeric",
			month: "short",
			year: "numeric",
		},
	},
	comments: {
		giscus: {
			repo: "PsiACE/psiace",
			repoId: "R_kgDOKYGbpA",
			category: "General",
			categoryId: "DIC_kwDOKYGbpM4CZxPW",
			mapping: "title",
			strict: "0",
			reactionsEnabled: "1",
			emitMetadata: "0",
			inputPosition: "top",
			theme: "preferred_color_scheme",
			lang: "en",
			loading: "lazy",
		},
	},
};

// Used to generate links in both the Header & Footer.
export const menuLinks: Array<{ title: string; path: string }> = [
	{
		title: "Home",
		path: "/",
	},
	{
		title: "About",
		path: "/about/",
	},
	{
		title: "Blog",
		path: "/posts/",
	},
];
