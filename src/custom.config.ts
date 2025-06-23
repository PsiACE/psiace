/**
 * Custom configuration for site-specific extensions
 * This file contains all customizations that extend the base Astro Cactus theme
 *
 * When updating the upstream theme, only this file and the /src/components/custom/
 * directory should need to be maintained.
 */

export interface CustomConfig {
	// Comments configuration
	comments: {
		enabled: boolean;
		provider: "giscus";
		giscus?: {
			repo: string;
			repoId: string;
			category: string;
			categoryId: string;
			mapping: string;
			strict: string;
			reactionsEnabled: string;
			emitMetadata: string;
			inputPosition: string;
			theme: string;
			lang: string;
			loading: string;
		};
	};

	// Social links configuration
	socialLinks: Array<{
		name: string;
		friendlyName: string;
		link: string;
		icon: string;
	}>;

	// Experience configuration
	experience: Array<{
		title: string;
		organization: string;
		organizationUrl: string;
		description: string;
		period: string;
		current?: boolean;
	}>;

	// Education configuration
	education: Array<{
		title: string;
		organization: string;
		organizationUrl: string;
		description: string;
		period: string;
	}>;

	// Projects configuration
	projects: Array<{
		title: string;
		organization: string;
		organizationUrl: string;
		description: string;
		period: string;
	}>;

	// Custom features flags
	features: {
		enableReadingTime: boolean;
		enableTOC: boolean;
		enableSearch: boolean;
		enableRSS: boolean;
	};

	// Page headers configuration
	pageHeaders: {
		[key: string]: {
			title?: string;
			subtitle?: string;
			description?: string;
			showSocialLinks?: boolean;
		};
	};
}

export const customConfig: CustomConfig = {
	comments: {
		enabled: true,
		provider: "giscus",
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

	socialLinks: [
		{
			name: "mdi:github",
			friendlyName: "Github",
			link: "https://github.com/psiace",
			icon: "mdi:github",
		},
		{
			name: "mdi:mastodon",
			friendlyName: "Mastodon",
			link: "https://fosstodon.org/@psiace",
			icon: "mdi:mastodon",
		},
		{
			name: "mdi:linkedin",
			friendlyName: "LinkedIn",
			link: "https://www.linkedin.com/in/psiace/",
			icon: "mdi:linkedin",
		},
		{
			name: "mdi:rss",
			friendlyName: "RSS",
			link: "https://psiace.me/rss.xml",
			icon: "mdi:rss",
		},
		{
			name: "mdi:email",
			friendlyName: "email",
			link: "mailto:psiace@outlook.com",
			icon: "mdi:email",
		},
	],

	experience: [
		{
			title: "GenAI Team Member",
			organization: "Vesoft Inc. (NebulaGraph)",
			organizationUrl: "https://github.com/vesoft-inc/",
			description: "Exploring the infrastructure and applications of AI and Graph",
			period: "Sep 2024 - Present",
			current: true,
		},
		{
			title: "Founding Member",
			organization: "Databend",
			organizationUrl: "https://github.com/datafuselabs/databend/",
			description: "Early employee and core contributor, building the future of cloud [Data + AI] analytics",
			period: "Jun 2021 - Aug 2024",
		},
		{
			title: "PMC Member",
			organization: "Apache OpenDAL™",
			organizationUrl: "https://github.com/apache/opendal",
			description: "Dedicated to creating a unified data access experience for developers",
			period: "",
		},
	],

	education: [
		{
			title: "Master's in Applied Mathematics and Data Science",
			organization: "Macau University of Science and Technology",
			organizationUrl: "https://www.must.edu.mo/",
			description: "Focus on machine learning, data analysis and mathematical modeling",
			period: "Sep 2022 - Aug 2024",
		},
		{
			title: "Bachelor's in Computer Science and Technology",
			organization: "Huazhong Agricultural University",
			organizationUrl: "https://www.hzau.edu.cn/",
			description: "Comprehensive study in computer science fundamentals and software engineering",
			period: "Sep 2017 - Jun 2021",
		},
	],

	projects: [
		{
			title: "Founding Member",
			organization: "Databend",
			organizationUrl: "https://github.com/datafuselabs/databend",
			description: "A modern cloud data warehouse focusing on reducing cost and complexity for your massive-scale analytics needs. Open source alternative to Snowflake.",
			period: "",
		},
		{
			title: "PMC Member",
			organization: "Apache OpenDAL™",
			organizationUrl: "https://github.com/apache/opendal",
			description: "A data access layer that allows users to easily and efficiently retrieve data from various storage services in a unified way.",
			period: "",
		},
		{
			title: "Owner",
			organization: "RiteRaft",
			organizationUrl: "https://github.com/riteraft/riteraft",
			description: "A raft framework, for regular people.",
			period: "",
		},
	],

	features: {
		enableReadingTime: true,
		enableTOC: true,
		enableSearch: true,
		enableRSS: true,
	},

	pageHeaders: {
		home: {
			title: "Hey, World!",
			description: "Passionate about open source, I thrive on building large-scale systems and exploring the intersection of data and AI. My journey is driven by an insatiable curiosity for knowledge and innovation.",
			showSocialLinks: true,
		},
		about: {
			title: "About",
			subtitle: "Hi, I'm Chojan Shang.",
			description: "Passionate about open source, I thrive on building large-scale systems and exploring the intersection of data and AI. My journey is driven by an insatiable curiosity for knowledge and innovation.",
			showSocialLinks: false,
		},
	},
};
