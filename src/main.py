import gemini
import utils


def main():
    gemini_endpoint = ""
    gemini_model = "gemini-2.5-flash"
    data_path = "data/test/data-jigsaw-10.csv"

    try:
        gemini_endpoint = utils.setup()
    except RuntimeError as e:
        print(e)

    data, targets = utils.readCSV(data_path)
    gemini.queryGemini(gemini_model, gemini_endpoint, data.to_string())
    results = utils.readCache("cache/query_results.json")
    utils.analysis(results,targets)


if __name__ == "__main__":
    main()
