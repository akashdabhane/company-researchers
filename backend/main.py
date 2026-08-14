from graph.graph import graph

def main():

    company_name = input(
        "Enter company name: "
    )

    website_url = input(
        "Enter company website URL: "
    )

    config = {
        "configurable": {
            "thread_id": "cli_user"
        }
    }

    result = graph.invoke(
        {
            "company_name": company_name,
            "website_url": website_url
        },
        config=config
    )

    print("\nFinal Report:\n")
    print(result)

if __name__ == "__main__":
    main()