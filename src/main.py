import query
import utils


def main():
    availableTasks = ["score", "analyse", "test"]
    envPath = ".env"

    # Config and api keys
    task = utils.readArgs(availableTasks)
    targetProvider, model, dataPath, cachePath = utils.readConfig("config.json")

    # Executing task
    try:
        match task:
            case "score":
                endpoint = utils.resolveEndpoints(envPath, targetProvider)
                data, targets = utils.readAndSeparateData(dataPath)
                # 32 is the optimal batch size for OpenAI endpoint
                results = query.queryOpenAI(endpoint, data, 32)
                utils.mergeAndCache(results, targets, cachePath)
                utils.verifyCacheIntegrity(dataPath, cachePath)
            case "analyse":
                # More complex analysis functionality still needs to be done...
                results = utils.readCache(cachePath)
                print(results.head(10))
            case "test":
                print("Testing...")
    except Exception as e:
        print(f"Error occured - {e}")


if __name__ == "__main__":
    main()
