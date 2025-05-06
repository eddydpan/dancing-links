# Dancing Links

Contributors: Gabe Zak, Vaani Bhatnagar, Eddy Pan

---

In this repository, we did a deep-dive on the Dancing Links algorithm (a.k.a
Algorithm X). We implemented it in Python and applied it to the following
LeetCode Hard Problems:

- **N-Queens** ([LeetCode 51](https://leetcode.com/problems/n-queens/))
- **N-Queens II** ([LeetCode 52](https://leetcode.com/problems/n-queens-ii/)),
- **Sudoku Solver**
  ([LeetCode 37](https://leetcode.com/problems/sudoku-solver/))

In our `report.ipynb`, you'll find a complete write-up on these implementations
and tests for them.

---

## Web Interface

Knuth mentions in his
[2018 lecture](https://www.youtube.com/watch?v=_cR9zDlvP88) he's _"... still
waiting for somebody to write an app that takes this algorithm and an exact
cover problem and somehow animates it..."_.

#### Interactive Demo

We're enthusiastic to announce that we've done just that: make sure to play
around with our visualizer demo available on our GitHub page available at
https://eddydpan.github.io/dancing-links/.

In order to create this demo, we ported the Python implementation to Javascript
and made a React front-end to make the interactive visualizer. All this code is
available in the `gh-pages` branch.

---

## Setup

To set up your environment, make sure you have Python (3.10+) downloaded and
installed. Next, clone this repository:

```bash
git clone git@github.com:eddydpan/dancing-links.git
```

And then in this repository directory, download the Python dependencies:

```bash
pip install -r requirements.txt
```

---

## More Resources

For an amazing slideshow that highlights aspects of our work over the course of
this project and demo problems that walks through the logic of DLX and the
LeetCode solutions, feel free to check out
[these google slides](https://docs.google.com/presentation/d/1AS5-agf4QNf9up3ARq-uBXr2tUAGxle65uFYnTdCQnU/edit?usp=sharing).

We built our conceptual understanding of Dancing Links through Dr. Don Knuth's
amazing online resources, such as
[this paper](https://arxiv.org/pdf/cs.DS/0011047) and
[this 2018 lecture](https://www.youtube.com/watch?v=_cR9zDlvP88).
