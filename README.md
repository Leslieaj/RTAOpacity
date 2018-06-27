# RTAOpacity

A simple tool for checking the opacity problems of Real-time automaton.

## The Opacity of Real-time Automata

### Basic information

It's a prototype tool for deciding the language-opacity of Real-time automata (**RTA**).

#### Some details

We reduce the decidability of language-opacity problem of RTA to the problem of inclusion of regular language, which is decidable form automaton theory.

At first, we have two real-time automaton $\mathcal{A}$ and $\mathcal{A}_{secret}$ , which stand for the system model and the model of secret part respectively. We transform them to two DFAs  $\mathcal{B}$ and $\mathcal{B}_{ns}$ (the two RTA is deterministic).  They accept languages trace-equivalent to $L(\mathcal{A})$ and $L(\mathcal{A})$ \ $L(\mathcal{A}_{secret})$.

At second, it is natural to obtain $\mathcal{B}|_{\Sigma_{0}}$ and $\mathcal{B}_{ns}|_{\Sigma_{0}}$ which accept projection acception languages on the observable actions set $\Sigma_{0}$ .

Finally, we apply the complement and product operations on them again, and obtain $\mathcal{B}|_{\Sigma_{0}} \times (\mathcal{B}_{ns}|_{\Sigma_{0}})^{comp}$. Clearly, $\mathcal{A}$ is language-opaque w.r.t. $\mathcal{A}_{secret}$ and $\Sigma_{0}$ if and only if $L_{f}{(\mathcal{B}|_{\Sigma_{0}} \times (\mathcal{B}_{ns}|_{\Sigma_{0}})^{comp})}$ is empty.

####Using guide

We test it on Linux (Ubuntu 16.04 64bit), but it is a pure python program.

Make sure the python version is 2.* (we test on python 2.7).

* Two model files are **a.json** and **a_secret.json**.

  ```json
  {
      "name": "A",
      "s": ["1", "2", "3"],
  	"sigma": ["a", "b"],
  	"tran": {
  		"0": ["1", "b", "[2,4]", "2"],
  		"1": ["1", "a", "[2,5]", "2"],
  		"2": ["2", "b", "[3,4]", "3"],
  		"3": ["2", "a", "[1,3]", "3"]
  	},
  	"init": "1",
  	"accept": ["3"],
  	"observable": ["a"]
  }
  ```

  There are 7 part in one RTA model.

  * "name" stands for the name of RTA.
  * "s" is a list of state names.
  * "sigma" is the alphabet.
  * "tran" is the list of transitions. A transition is in the form "id : [source, label, guard, target].
  * "init" stands the name of the init state
  * "accept" means the  list of the names of accept states.
  * "observable" is the list of observable actions. **MAKE SURE two models have the same one list** .

* Then we can run:

  ```python
  python opacity.py a.json a_secret.json
  ```

  If the result is "**Language Opaque!** ", then it means RTA $\mathcal{A}$ is language-opaque w.r.t $L(\mathcal{A}_{secret})$ and $\Sigma_{0}$.

  If the result is "**NOT!**", then it means RTA $\mathcal{A}$ is not language-opaque w.r.t $L(\mathcal{A}_{secret})$ and $\Sigma_{0}$.

  * We may print final product automaton and its refined one.
  * We also print the total time in seconds.