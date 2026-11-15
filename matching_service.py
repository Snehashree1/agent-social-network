import re
import math
from collections import Counter


STOP_WORDS = {
    "and", "or", "the", "a", "an", "in", "on",
    "for", "to", "of", "with", "is", "are",
    "this", "that", "during", "get", "using"
}


def normalize_word(word):
    """Convert simple plurals into their base form."""
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"

    if len(word) > 4 and word.endswith("s"):
        return word[:-1]

    return word


def extract_terms(text):
    words = re.findall(r"[a-z0-9]+", text.lower())

    return [
        normalize_word(word)
        for word in words
        if word not in STOP_WORDS and len(word) > 1
    ]


def get_post_text(post):
    return " ".join([
        post.get("title", ""),
        post.get("content", ""),
        post.get("category", ""),
        " ".join(post.get("keywords", []))
    ])


def get_agent_text(agent):
    return " ".join([
        agent.get("description", ""),
        " ".join(agent.get("interests", [])),
        " ".join(agent.get("keywords", []))
    ])


def cosine_similarity(vector1, vector2):
    dot_product = sum(
        vector1.get(word, 0) * vector2.get(word, 0)
        for word in vector1
    )

    magnitude1 = math.sqrt(sum(value ** 2 for value in vector1.values()))
    magnitude2 = math.sqrt(sum(value ** 2 for value in vector2.values()))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)


def find_relevant_agents(post, agents, threshold=15):

    post_terms = extract_terms(get_post_text(post))
    post_counts = Counter(post_terms)

    other_agents = [
        agent for agent in agents
        if agent["agent_id"] != post["agent_id"]
    ]

    agent_documents = [
        extract_terms(get_agent_text(agent))
        for agent in other_agents
    ]

    documents = [post_terms] + agent_documents
    total_documents = len(documents)

    # Calculate inverse document frequency
    document_frequency = Counter()

    for document in documents:
        document_frequency.update(set(document))

    def create_vector(terms):
        counts = Counter(terms)
        total_terms = len(terms)

        if total_terms == 0:
            return {}

        vector = {}

        for word, count in counts.items():
            tf = count / total_terms
            idf = math.log(
                (total_documents + 1) /
                (document_frequency[word] + 1)
            ) + 1

            vector[word] = tf * idf

        return vector

    post_vector = create_vector(post_terms)
    results = []

    for agent, agent_terms in zip(other_agents, agent_documents):

        agent_vector = create_vector(agent_terms)

        similarity = cosine_similarity(
            post_vector,
            agent_vector
        )

        score = round(similarity * 100, 2)

        matched_terms = sorted(
            set(post_terms).intersection(set(agent_terms))
        )

        if score >= threshold:

            results.append({
                "agent_id": agent["agent_id"],
                "agent_name": agent["agent_name"],
                "company": agent["company"],
                "relevance_score": score,
                "matched_terms": matched_terms
            })

    results.sort(
        key=lambda item: item["relevance_score"],
        reverse=True
    )

    return results
