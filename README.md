# News-AIgency

## How to run pre-commit locally

Install new dependencies in requirements and then:
1. pre-commit install
2. a) pre-commit run --all-files
*or*
2. b) runs with every git commit
3. The files that are not automatically updated need to be manually updated. If they are not updated it won't allow you to commit.

## Endpoint documentation

### Summary of Endpoints

- [Health Check](#endpoint-health-check): Checks the health status of the API.
- [Info](#endpoint-info): Retrieves the application's name and version.
- [Test LiteLLM](#endpoint-test-litellm): Tests the LiteLLM service and returns a short poem.
- [URL Domain Validation](#endpoint-url-domain-validation): Validates if the provided URL is from a trusted hostname.
- [Generate Topics](#endpoint-generate-topics): Generates topics from a given article URL.
- [Generate Article](#endpoint-generate-article): Generates an article based on a given URL and topic.
- [Generate Headlines](#endpoint-generate-headlines): Generates headlines for a given article.
- [Regenerate Headlines](#endpoint-regenerate-headlines): Regenerates headlines for a given article.
- [Generate Engaging Text](#endpoint-generate-engaging-text): Generates engaging text for a given article.
- [Regenerate Engaging Text](#endpoint-regenerate-engaging-text): Regenerates engaging text for a given article.
- [Generate Perex](#endpoint-generate-perex): Generates a perex for a given article.
- [Regenerate Perex](#endpoint-regenerate-perex): Regenerates a perex for a given article.
- [Generate Article Body](#endpoint-generate-article-body): Generates the body of an article.
- [Regenerate Article Body](#endpoint-regenerate-article-body): Regenerates the body of an article.
- [Generate Tags](#endpoint-generate-tags): Generates tags for a given article.
- [Regenerate Tags](#endpoint-regenerate-tags): Regenerates tags for a given article.

### Endpoint: Health Check

#### URL

`/health`

#### Method
- **GET**

#### Description
Checks the health status of the API.

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "status": "OK"
  }
  ```

### Endpoint: Info

#### URL

`/info`

#### Method
- **GET**

#### Description
Retrieves the application's name and version.

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "app_name": "News AIgency",
    "version": "v1"
  }
  ```

### Endpoint: Test LiteLLM

#### URL

`/use-litellm`

#### Method
- **GET**

#### Description
Tests the LiteLLM service and returns a short poem.

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "LiteLLM Response": "In the hush of twilight's glow,  \nWhispers dance on breezes slow,  \nStars awaken, one by one,  \nNight unfolds, the day is done.  \n\nMoonlight spills like silver lace,  \nPainting shadows, soft embrace,  \nIn this moment, time stands still,  \nMagic lingers, heartbeats thrill.  "
  }
  ```

### Endpoint: URL Domain Validation

#### URL

`/url-validate`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Validates if the provided URL is from a trusted hostname.

#### Parameters

##### Query Parameters

| Parameter  | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| `url`      | string | No       | URL to validate. Default is a sample URL. |
| `hostnames`| list   | No       | List of trusted hostnames.               |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "detail": "<validated_url>"
  }
  ```

### Endpoint: Generate Topics

#### URL

`/article/topics`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Generates 5 (*can be adjusted*) topics from a given article URL using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter | Type   | Required | Description                                                      |
|-----------|--------|----------|------------------------------------------------------------------|
| `url`     | string | No       | URL of the article to generate topics from. Default is a sample URL. |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
  }
  ```

### Endpoint: Generate Article

#### URL

`/article/generate`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Generates an article based on a given URL and topic using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter       | Type   | Required | Description                                                      |
|-----------------|--------|----------|------------------------------------------------------------------|
| `url`           | string | No       | URL of the article to generate content from. Default is a sample URL. |
| `selected_topic`| string | No       | The selected topic for the article. Default is a sample topic.   |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "headlines": ["Headline 1", "Headline 2", "Headline 3"],
    "engaging_text": "Engaging text to hook the reader",
    "perex": "Introductory text to the article.",
    "article": "The article itself in one block of text. Newlines are indicated with '\n'.",
    "tags": ["#TAG1", "#TAG2", "#TAG3", "#TAG4"]
  }
  ```

### Endpoint: Generate Headlines

#### URL

`/generate/headlines`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Generates headlines for a given article URL and selected topic using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter       | Type   | Required | Description                                                      |
|-----------------|--------|----------|------------------------------------------------------------------|
| `url`           | string | No       | URL of the article to generate headlines from. Default is a sample URL. |
| `selected_topic`| string | No       | The selected topic for the headlines. Default is a sample topic. |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "headlines": ["Headline 1", "Headline 2", "Headline 3"]
  }
  ```

### Endpoint: Regenerate Headlines

#### URL

`/regenerate/headlines`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Regenerates headlines for a given article URL and selected topic using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter        | Type   | Required | Description                                                      |
|------------------|--------|----------|------------------------------------------------------------------|
| `url`            | string | No       | URL of the article to regenerate headlines from. Default is a sample URL. |
| `selected_topic` | string | No       | The selected topic for the headlines. Default is a sample topic. |
| `old_headlines`  | string | No       | Old headlines to regenerate from.                                |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "headlines": ["New Headline 1", "New Headline 2", "New Headline 3"]
  }
  ```

### Endpoint: Generate Engaging Text

#### URL

`/generate/engaging_text`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Generates engaging text for a given article URL, selected topic, and current headline using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter          | Type   | Required | Description                                                      |
|--------------------|--------|----------|------------------------------------------------------------------|
| `url`              | string | No       | URL of the article to generate engaging text from. Default is a sample URL. |
| `selected_topic`   | string | No       | The selected topic for the engaging text. Default is a sample topic. |
| `current_headline` | string | No       | The current headline for the article. Default is a sample headline. |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "engaging_text": "Engaging text to hook the reader"
  }
  ```

### Endpoint: Regenerate Engaging Text

#### URL

`/regenerate/engaging_text`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Regenerates engaging text for a given article URL, selected topic, old engaging text, and current headline using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter            | Type   | Required | Description                                                      |
|----------------------|--------|----------|------------------------------------------------------------------|
| `url`                | string | No       | URL of the article to regenerate engaging text from. Default is a sample URL. |
| `selected_topic`     | string | No       | The selected topic for the engaging text. Default is a sample topic. |
| `old_engaging_text`  | string | No       | The old engaging text to regenerate from. Default is sample engaging text. |
| `current_headline`   | string | No       | The current headline for the article. Default is a sample headline. |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "engaging_text": "New engaging text to hook the reader"
  }
  ```

### Endpoint: Generate Perex

#### URL

`/generate/perex`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Generates a perex (introductory text) for a given article URL, selected topic, and current headline using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter          | Type   | Required | Description                                                      |
|--------------------|--------|----------|------------------------------------------------------------------|
| `url`              | string | No       | URL of the article to generate perex from. Default is a sample URL. |
| `selected_topic`   | string | No       | The selected topic for the perex. Default is a sample topic.     |
| `current_headline` | string | No       | The current headline for the article. Default is a sample headline. |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "perex": "Introductory text to the article."
  }
  ```

### Endpoint: Regenerate Perex

#### URL

`/regenerate/perex`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Regenerates a perex for a given article URL, selected topic, old perex, and current headline using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter        | Type   | Required | Description                                                      |
|------------------|--------|----------|------------------------------------------------------------------|
| `url`            | string | No       | URL of the article to regenerate perex from. Default is a sample URL. |
| `selected_topic` | string | No       | The selected topic for the perex. Default is a sample topic.     |
| `old_perex`      | string | No       | The old perex to regenerate from. Default is a sample perex.     |
| `current_headline`| string | No      | The current headline for the article. Default is a sample headline. |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "perex": "New introductory text to the article."
  }
  ```

### Endpoint: Generate Article Body

#### URL

`/generate/articlebody`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Generates the body of an article for a given URL, selected topic, and current headline using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter          | Type   | Required | Description                                                      |
|--------------------|--------|----------|------------------------------------------------------------------|
| `url`              | string | No       | URL of the article to generate the body from. Default is a sample URL. |
| `selected_topic`   | string | No       | The selected topic for the article body. Default is a sample topic. |
| `current_headline` | string | No       | The current headline for the article. Default is a sample headline. |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "article_body": "The article body text. Newlines are indicated with '\n'."
  }
  ```

### Endpoint: Regenerate Article Body

#### URL

`/regenerate/articlebody`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Regenerates the body of an article for a given URL, selected topic, old article body, and current headline using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter          | Type   | Required | Description                                                      |
|--------------------|--------|----------|------------------------------------------------------------------|
| `url`              | string | No       | URL of the article to regenerate the body from. Default is a sample URL. |
| `selected_topic`   | string | No       | The selected topic for the article body. Default is a sample topic. |
| `old_article_body` | string | No       | The old article body to regenerate from. Default is the sample article body. |
| `current_headline` | string | No       | The current headline for the article. Default is a sample headline. |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "article_body": "The new article body text. Newlines are indicated with '\n'."
  }
  ```

### Endpoint: Generate Tags

#### URL

`/generate/tags`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Generates tags for a given article URL, selected topic, current headline, and article body using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter          | Type   | Required | Description                                                      |
|--------------------|--------|----------|------------------------------------------------------------------|
| `url`              | string | No       | URL of the article to generate tags from. Default is a sample URL. |
| `selected_topic`   | string | No       | The selected topic for the tags. Default is a sample topic.      |
| `current_headline` | string | No       | The current headline for the article. Default is a sample headline. |
| `current_article`  | string | No       | The current article body. Default is the sample article.         |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "tags": ["#TAG1", "#TAG2", "#TAG3", "#TAG4"]
  }
  ```

### Endpoint: Regenerate Tags

#### URL

`/regenerate/tags`

#### Method
- **GET**: *development only*
- **POST**

#### Description
Regenerates tags for a given article URL, selected topic, old tags, current headline, and article body using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter          | Type   | Required | Description                                                      |
|--------------------|--------|----------|------------------------------------------------------------------|
| `url`              | string | No       | URL of the article to regenerate tags from. Default is a sample URL. |
| `selected_topic`   | string | No       | The selected topic for the tags. Default is a sample topic.      |
| `old_tags`         | list   | No       | The old tags to regenerate from. Default is the sample tags.     |
| `current_headline` | string | No       | The current headline for the article. Default is a sample headline. |
| `current_article`  | string | No       | The current article body. Default is the sample article.         |

#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  ```json
  {
    "tags": ["#NewTAG1", "#NewTAG2", "#NewTAG3", "#NewTAG4"]
  }
  
