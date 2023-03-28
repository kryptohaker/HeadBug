# HeadBug (Web Header Security Checker)
HeadBug is a Python-based tool designed to check the security of web headers and cookies based on the best practices - e.g., guidelines from OWASP and Mozilla. It helps identify potential security issues in the HTTP headers and cookies of a target website.

## Features
- Checks target site headers for security best practices
- Supports custom header checks through JSON files
- Analyzes cookies for security best practices
- Provides recommendations based on OWASP and Mozilla guidelines
- Supports custom request headers (e.g., for authorization)

## Requirements
- Python 3.6 or higher

## Usage
1. Clone this repository or download the `headbug.py` script.
2. Create the following directories in the same location as the `headbug.py` script:
- `recommendations`: for header recommendations in JSON format
- `cookie_recommendations`: for cookie recommendations in JSON format
3. Add JSON files with recommendations to the respective folders.
4. Run the script using the following command:

```bash
python headbug.py target_url [custom_headers.json]
```
- `target_url`: The URL of the website you want to analyze.
- `custom_headers.json` (optional): A JSON file containing custom headers to be included in the request.

The script will output a list of identified security issues based on the JSON recommendations provided.

Example of custom_headers.json file with an Authorization header using the Bearer token scheme:
```json
{
  "Authorization": "Bearer your_jwt_token_here"
}
```

>Remember that not all recommendations may apply to every application, and you should review and adjust these recommendations based on your specific requirements and threat model.

## How to create a JSON file for checking of header

Here is a step-by-step guide to creating a JSON file for checking the `X-Content-Type-Options` header:

1. Create a new text file and save it with the .json extension. Name the file `X_Content_Type_Options.json`. The name should be descriptive of the header you are checking.
2. In the JSON file, define an object with three properties: `header`, `missing_message`, and `check`.
- `header`: This property specifies the name of the HTTP header you want to check. In this case, it's "**X-Content-Type-Options**".
- `missing_message`: This property contains a message that will be displayed if the header is missing. For example, "**X-Content-Type-Options header is missing. Consider adding it with the value 'nosniff' to prevent MIME type sniffing.**". 
- `check`: This property holds a Python lambda function as a string. The lambda function takes the header value as an argument and returns a list of recommendations. For the `X-Content-Type-Options header`, the lambda function checks if the header value is not equal to nosniff and returns a recommendation accordingly: "**lambda value: ['X-Content-Type-Options should be set to nosniff.'] if value.lower() != 'nosniff' else []**".
3. Once you have defined the object with the necessary properties, your JSON file should look like this:

```json
{
  "header": "X-Content-Type-Options",
  "missing_message": "X-Content-Type-Options header is missing. Consider adding it with the value 'nosniff' to prevent MIME type sniffing.",
  "check": "lambda value: ['X-Content-Type-Options should be set to nosniff.'] if value.lower() != 'nosniff' else []"
}
```
4. Save the JSON file in the `recommendations` folder of HeadBug project. The script will read this file and use the defined checks to analyze the `X-Content-Type-Options` header for the target website.

This JSON file will be read by the HeadBug script, and the recommendations will be generated based on the header value and the check defined in the check property.

## Contributing
Feel free to submit pull requests to improve the tool or add more recommendations. Always ensure that your recommendations are based on trusted sources like OWASP and Mozilla, and that they are relevant to the specific needs of web applications.

## License
This project is released under the MIT License. See the `LICENSE` file for more details.