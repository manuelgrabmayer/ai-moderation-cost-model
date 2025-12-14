import gemini
import utils


def main():
    # Could be moved to a config file
    gemini_endpoint = ""
    gemini_model = "gemini-2.5-flash"
    data_path = "data/test/data-jigsaw-10.csv"
    result_cache_path = "cache/query_results.json"

    # Load API keys
    try:
        gemini_endpoint = utils.setup()
    except RuntimeError as e:
        print(e)

    # Reading data file and projections
    data, targets = utils.readCSV(data_path)
    # LLM query
    # Might want to comment this line when doing analysis to save quota
    gemini.queryGemini(gemini_model, gemini_endpoint, data.to_string(), result_cache_path)

    # Reading .json cache and converting to pandas dataframe
    results = utils.readCache(result_cache_path)
    # Joining query results and targets and prining to stdout
    utils.analysis(results,targets)


if __name__ == "__main__":
    main()
