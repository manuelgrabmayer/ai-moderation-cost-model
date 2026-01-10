import analyse
import query
import utils


def main():
    availableTasks = ["score", "analyse", "test"]
    envPath = ".env"

    # Config and api keys
    task = utils.readArgs(availableTasks)
    targetProvider, model, dataPath, cachePath = utils.readConfig("config.json")
    rowLimit = 500
    continueFromCache = False
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
                scoredMessages = query.queryOpenAI(endpoint, messages, 5)

                # Caching and validation
                utils.mergeAndCache(scoredMessages, targets, cache, cachePath)
                utils.verifyCacheIntegrity(dataPath, cachePath)
            case "analyse":
                # More complex analysis functionality still needs to be done...
                scoredMessages = utils.readCache(cachePath)
                analyse.visualise(scoredMessages)
            case "test":
                print("Testing...")
                utils.verifyCacheIntegrity(dataPath, cachePath)
    except Exception as e:
        print(f"Error occured - {e}")


if __name__ == "__main__":
    main()
