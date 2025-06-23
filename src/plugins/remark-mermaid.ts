import { visit } from "unist-util-visit";
import type { Code, Root } from "mdast";

export function remarkMermaid() {
	return (tree: Root) => {
		visit(tree, "code", (node: Code, index, parent) => {
			if (node.lang === "mermaid") {
				// Replace the code block with a custom div that will be processed by mermaid
				const mermaidDiv = {
					type: "html",
					value: `<div class="mermaid">${node.value}</div>`,
				};

				if (parent && typeof index === "number") {
					parent.children[index] = mermaidDiv as any;
				}
			}
		});
	};
}
