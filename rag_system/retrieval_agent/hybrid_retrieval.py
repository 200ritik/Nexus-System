import logging

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Reciprocal Rank Fusion
# --------------------------------------------------

def reciprocal_rank_fusion(
    dense_results: list[dict],
    sparse_results: list[dict],
    top_k: int = 5,
    rrf_k: int = 60,
) -> list[dict]:
    """
    Combine dense and sparse search results
    using Reciprocal Rank Fusion (RRF).
    """

    fused_results = {}

    # --------------------------------------------------
    # Add dense results
    # --------------------------------------------------

    for result in dense_results:

        chunk_id = result.get("chunk_id")

        if not chunk_id:
            continue

        rank = result.get("rank")

        if chunk_id not in fused_results:

            fused_results[chunk_id] = {
                "chunk_id": chunk_id,
                "rrf_score": 0.0,
                "dense_score": None,
                "sparse_score": None,
                "metadata": result.get(
                    "metadata",
                    {},
                ),
            }

        fused_results[chunk_id]["rrf_score"] += (
            1 / (rrf_k + rank)
        )

        fused_results[chunk_id]["dense_score"] = (
            result.get("score")
        )

    # --------------------------------------------------
    # Add sparse results
    # --------------------------------------------------

    for result in sparse_results:

        chunk_id = result.get("chunk_id")

        if not chunk_id:
            continue

        rank = result.get("rank")

        if chunk_id not in fused_results:

            fused_results[chunk_id] = {
                "chunk_id": chunk_id,
                "rrf_score": 0.0,
                "dense_score": None,
                "sparse_score": None,
                "metadata": result.get(
                    "metadata",
                    {},
                ),
            }

        fused_results[chunk_id]["rrf_score"] += (
            1 / (rrf_k + rank)
        )

        fused_results[chunk_id]["sparse_score"] = (
            result.get("score")
        )

    # --------------------------------------------------
    # Sort by RRF score
    # --------------------------------------------------

    final_results = sorted(
        fused_results.values(),
        key=lambda result: result["rrf_score"],
        reverse=True,
    )

    # --------------------------------------------------
    # Return final Top-K
    # --------------------------------------------------

    final_results = final_results[:top_k]

    logger.info(
        "RRF fusion completed | results=%d",
        len(final_results),
    )

    return final_results