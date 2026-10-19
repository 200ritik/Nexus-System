# docling hybrid chunking   
import logging
from typing import Any

from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import (
    HuggingFaceTokenizer,
)
from transformers import AutoTokenizer

# ==========================================================================
    # CONFIHURATION
# ==========================================================================

logger = logging.getLogger(__name__)
TOKENIZER_NAME = "BAAI/bge-m3"
MAX_TOKENS = 384


# creating tokenizer module-----------------

def create_tokenizer()->HuggingFaceTokenizer:
    """ creating the tokens for to count the token so that the chunking works
    effectively without loosing any meaning
        HuggingFaceTokenizer: Pre existed tokenizer model
    """
    
    tokenizer = AutoTokenizer.from_pretrained(
        TOKENIZER_NAME
    )
    
    return HuggingFaceTokenizer(
        tokenizer = tokenizer,
        max_tokens=MAX_TOKENS,
    )

# hybrid chunker---------------------------------------------------

def create_chunker()->HybridChunker:
    """create the hybrid chunker function with struture awareness part

    Returns:
        HybridChunker: have the poperty of hybrid chunking + structure awareness
    """
    tokenizer = create_tokenizer()
    
    return HybridChunker(
        tokenizer = tokenizer,
        max_tokens = MAX_TOKENS,
        
        # table properties -------------
        repeat_table_header=True,
        # keep header with the rows ---------
        omit_header_on_overflow=False,
    )
    
# ===================================================================================
#  EXTRACT METADATA
# ===================================================================================

def extract_metadata(chunk: Any) -> dict:
    """
    chunk.meta.export_json_dict(): 
    It attempts to call a built-in Docling method that converts the chunk's internal metadata 
    (like page numbers, font styles, or bounding boxes) into a standard Python dict
    
    """

    try:
        return chunk.meta.export_json_dict()

    except Exception as error:

        logger.debug(
            "Could not export chunk metadata | error=%s",
            error,
        )

        return {}    

# ====================================================================
# chunking the one document 
# ====================================================================

def chunk_document(
    document: Any,
    chunker: HybridChunker,
    document_id: str | None = None,
    file_name: str | None = None,
) -> list[dict]:
    
    
    """ This function chunk the single document at a time and attach the metadata along with them 

    Args:
        document (Any): parsed document
        chunker (HybridChunker): docling hybrid chunker function 2
        document_id (str | None, optional): parsed document document id
        file_name (str | None, optional): Actual file name of the parsed document

    Returns:
        list[dict]: gives the list[dict] of data.....................
    """
    
    logger.info("Hybrid chunking started | file=%s", file_name,)
    chunks = []
    
    for chunk_index, chunk in enumerate(
        chunker.chunk(document)
    ):
        text = chunk.text.strip()
        
        if not text:
            continue
        
        metadata = extract_metadata(chunk)
        
        chunks.append(
            {
                "chunk_index" : chunk_index,
                "document_id" : document_id,
                "file_name" : file_name,
                "text" : text,
                "metadata" : metadata
            }
        )
        
    logger.info(
        "chunking sucessfull"
    )
    
    return chunks


# ================================================================================
# Multiple-document chunking
# ================================================================================

def chunks_documents(
    parsed_files : list[dict]
)->list[dict]:
    """ Performing chunking on multiple documents

    Args:
        parsed_files (list[dict]): Actual docling parsed files

    Returns:
        list[dict]: chunks + metedata + extra info
    """
    
    
    if not parsed_files:
        logger.warning("no parsed files document supplied")
        return []
    
    logger.info("multiple file HybridChunking started | documents=%d",len(parsed_files),)
    
    
    chunker = create_chunker()
    all_chunks=[]
    
    for files in parsed_files:
        
        file_name = files.get("file_name")
        document_id = files.get("document_id")
        document = files.get("document")
        
        if document is None:
            logger.warning("No docling document found | file%s", file_name)
            
            continue
        try:
            chunks = chunk_document(
                document=document,
                chunker=chunker,
                document_id=document_id,
                file_name=file_name
            )
            all_chunks.extend(chunks)
            
        except Exception as error:
            logger.error("Chunking failed | file = %s | error=%s", file_name, error, exc_info=True)
            
            continue
        
    logger.info("Hybrid chunking finished sucessfull | total_chunks=%d", len(all_chunks))
    return all_chunks