import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked_pages = corpus[page]
    all_pages = list(corpus.keys())
    prob_dist = {}
    if len(linked_pages) > 0:
        prob_damp = damping_factor/len(linked_pages)
        prob_random = (1 - damping_factor)/len(linked_pages)
        for cpage in all_pages:
            prob_dist[cpage] = prob_random + (prob_damp if cpage in linked_pages else 0)
    else:
        prob_dist = dict.fromkeys(all_pages,1/len(all_pages))
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus.keys())
    page_count_dict = dict.fromkeys(all_pages, 0)
    page = random.choice(all_pages)
    for i in range(n):
        page_count_dict[page] += 1
        prob_dist = transition_model(corpus, page, damping_factor)
        pages, probabilities = zip(*prob_dist.items())
        page = random.choices(pages, weights=probabilities, k=1)[0]
    page_rank_dict = {k: v / n for k, v in page_count_dict.items()}
    return page_rank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    initial_rank = 1 / num_pages
    random_choice_prob = (1 - damping_factor) / num_pages
    page_ranks = {page_name: initial_rank for page_name in corpus}
    new_ranks = {page_name: 0 for page_name in corpus}
    max_rank_change = initial_rank
    while max_rank_change > 0.001:
        max_rank_change = 0
        for page_name in corpus:
            surf_choice_prob = 0
            for other_page in corpus:
                if len(corpus[other_page]) == 0:
                    surf_choice_prob += page_ranks[other_page] / num_pages
                elif page_name in corpus[other_page]:
                    surf_choice_prob += page_ranks[other_page] / len(corpus[other_page])
            new_rank = random_choice_prob + (damping_factor * surf_choice_prob)
            new_ranks[page_name] = new_rank
        normal_factor = sum(new_ranks.values())
        new_ranks = {page: (rank / normal_factor) for page, rank in new_ranks.items()}
        for page_name in corpus:
            rank_change = abs(page_ranks[page_name] - new_ranks[page_name])
            if rank_change > max_rank_change:
                max_rank_change = rank_change
        page_ranks = new_ranks.copy()
    return page_ranks


if __name__ == "__main__":
    main()
