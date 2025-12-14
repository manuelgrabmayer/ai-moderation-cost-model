import gemini
import utils


def main():
    gemini_endpoint = ""
    gemini_model = "gemini-2.5-flash"

    try:
        gemini_endpoint = utils.setup()
    except RuntimeError as e:
        print(e)

    data = utils.readCSV("data/full/data-jigsaw.csv", 10)
    gemini.queryGemini(gemini_model, gemini_endpoint, data)


if __name__ == "__main__":
    main()
