import analyse
import query
import utils


def main():
    availableTasks = ["score", "analyse", "test"]
    envPath = ".env"

    # Config and api keys
    task = utils.readArgs(availableTasks)
    targetProvider, model, dataPath, cachePath = utils.readConfig("config.json")
    rowLimit = 8000
    continueFromCache = True
    # Executing task
    try:
        match task:
            case "score":
                # Endpoints
                endpoint = utils.resolveEndpoints(envPath, targetProvider)

                # Fetch data
                if continueFromCache:
                    data, cache = utils.fetchData(dataPath, rowLimit, cachePath)
                else:
                    data, cache = utils.fetchData(dataPath, rowLimit)

                # Already scored?
                if data is None:
                    return

                messages, targets = utils.separateData(data)

                # Query
                # 32 is the optimal batch size for OpenAI endpoint
                scoredMessages = query.queryOpenAI(endpoint, messages, 32)

                # Caching and validation
                utils.mergeAndCache(scoredMessages, targets, cache, cachePath)
                utils.verifyCacheIntegrity(dataPath, cachePath)
            case "analyse":
                # More complex analysis functionality still needs to be done...
                data = utils.readCache(cachePath)
                scoreColumns = [column for column in data.columns if "OPENAI_" in column]

                model_scores = data["OPENAI_hate/threatening"]#data[scoreColumns].max(axis=1)
                target_scores = data["JIGSAW_threat"]#data["JIGSAW_target"]

                thresholdCount = 100
                results = analyse.threshold(target_scores,model_scores,thresholdCount)
                results["FPR"] = results["FP"] / (results["FP"] + results["TN"])
                results["FNR"] = results["FN"] / (results["FN"] + results["TP"])

                analyse.visualise(results)
            case "test":
                print("Testing...")
    except Exception as e:
        print(f"Error occured - {e}")


if __name__ == "__main__":
    main()
