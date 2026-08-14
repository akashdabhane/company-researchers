from langchain_core.tools import tool
import wikipedia


@tool
def search_wikipedia(query: str) -> dict:
    """
    Search Wikipedia for general information about a person, company, or topic.
    Use this to get background information when YouTube data alone is not enough.
    Returns a summary and the page URL.
    """
    try:
        wikipedia.set_user_agent("wikipedia-agent/1.0")
        
        results = wikipedia.search(query, results=3)
        
        if not results:
            return {"error": f"No Wikipedia results found for: {query}"}
        
        page = wikipedia.page(results[0], auto_suggest=False)
        
        return {
            "title": page.title,
            "summary": page.summary[:500],
            "url": page.url,
        }

    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple matches — pick the first one
        try:
            page = wikipedia.page(e.options[0], auto_suggest=False)
            return {
                "title": page.title,
                "summary": page.summary[:500],
                "url": page.url,
            }
        except Exception:
            return {"error": f"Disambiguation error for: {query}. Options: {e.options[:3]}"}

    except wikipedia.exceptions.PageError:
        return {"error": f"No Wikipedia page found for: {query}"}

    except Exception as e:
        return {"error": f"Wikipedia lookup failed: {str(e)}"}



@tool
def wikipedia_search(query: str) -> list:
    """
    Search Wikipedia and return matching page titles.
    Useful when exact company page name is unknown.
    """

    try:
        return wikipedia.search(query, results=10)

    except Exception as e:
        return [f"Error: {str(e)}"]


@tool
def wikipedia_summary(company_name: str) -> str:
    """
    Get a concise Wikipedia summary of a company.
    Useful for quick company overview. 
    """

    try:
        return wikipedia.summary(
            company_name,
            sentences=5,
            auto_suggest=True
        )

    except wikipedia.DisambiguationError as e:
        return (
            f"Multiple matches found.\n"
            f"Possible pages: {e.options[:10]}"
        )

    except wikipedia.PageError:
        return "Wikipedia page not found."

    except Exception as e:
        return f"Error: {str(e)}"


@tool
def wikipedia_full_content(company_name: str) -> str:
    """
    Retrieve full Wikipedia article content.
    Useful for deep company research.
    """

    try:
        page = wikipedia.page(
            company_name,
            auto_suggest=True
        )

        return page.content

    except wikipedia.DisambiguationError as e:
        return (
            f"Multiple matches found.\n"
            f"Possible pages: {e.options[:10]}"
        )

    except wikipedia.PageError:
        return "Wikipedia page not found."

    except Exception as e:
        return f"Error: {str(e)}"


@tool
def wikipedia_company_metadata(company_name: str) -> dict:
    """
    Extract structured metadata about a company from Wikipedia.
    This can include infobox data like industry, founded date, key people, etc.
    """

    try:
        page = wikipedia.page(
            company_name,
            auto_suggest=True
        )

        return {
            "title": page.title,
            "url": page.url,
            "categories": page.categories[:20],
            "links": page.links[:50],
        }

    except wikipedia.DisambiguationError as e:
        return {
            "error": "Disambiguation",
            "options": e.options[:10]
        }

    except wikipedia.PageError:
        return {"error": "Page not found"}

    except Exception as e:
        return {"error": str(e)}


@tool
def wikipedia_related_companies(company_name: str) -> list:
    """
    Find potentially related companies and organizations
    from internal Wikipedia links.
    """

    try:
        page = wikipedia.page(
            company_name,
            auto_suggest=True
        )

        links = page.links

        return links[:100]

    except Exception as e:
        return [f"Error: {str(e)}"]


@tool
def wikipedia_page_url(company_name: str) -> str:
    """
    Get the URL of the company's Wikipedia page.
    Useful for referencing the source of information.
    """

    try:
        page = wikipedia.page(
            company_name,
            auto_suggest=True
        )

        return page.url

    except Exception as e:
        return f"Error: {str(e)}"
    
    