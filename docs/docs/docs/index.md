Seamless integration and composability for large language model apps.

## Features
* Composable prompts and chains
    * Use multiple models to run one chain and then use that as input for a different chain and model
* Customizable prompt and response formatting
    * Add modifiers to prompts to change the style, length, and format of the response
    * Extract data from the response to use in the next prompt
    * Add custom functions to process the response
    * Add custom functions to process the input variables
* [Integration with OpenAI API (llama.cpp in progress)](./integrations.md)
* [Async calls to models](./async.md)
* [Run experiments to compare model parameters and performance over time](./experiments.md)

{% include-markdown '../../../README.md' start='<!--docs-index-start-->' end='<!--docs-index-end-->' %}
