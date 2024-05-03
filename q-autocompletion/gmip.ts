const branches: Fig.Generator = {
  script: ["git", "branch", "--no-color"],
  postProcess: (output) => {
    if (output.startsWith("fatal:")) {
      return [];
    }
    return output.split("\n").map((branch) => {
      return { name: branch.replace("*", "").trim(), description: "Branch" };
    });
  },
};

const completionSpec: Fig.Spec = {
  name: "gmip",
  description: "Merge current branch to target branch and push.",
  subcommands: [],
  options: [{
    name: ["--help", "-h"],
    description: "Show help for gmip",
  }],
  args: {
    name: "TARGET_BRANCH",
    description: "The branch to merge into.",
    generators: branches
  },
};
export default completionSpec;
