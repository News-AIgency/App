# News-AIgency

## How to run pre-commit locally

Install new dependies in requirements and then:
1. pre-commit install
2. a) pre-commit run --all-files
*or*
2. b) runs with every git commit
3. The files that are not automatically updated need to be manually updated. If they are not updated it wont allowed you to commit.

## Endpoint documentation

### Endpoint: Health Check

#### URL

`GET /health`

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

### Endpoint: Info

#### URL

`GET /info`

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

### Endpoint: Test LiteLLM

#### URL

`GET /use-litellm`

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

### Endpoint: Generate topics from URL

#### URL

`GET /article/topics`

#### Method
- **GET**: *temporary*
- **POST**

#### Description
Generates 5 (*can be adjusted*) topics from a given article URL using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter | Type   | Required | Description                                                      |
|-----------|--------|----------|------------------------------------------------------------------|
| `url`     | string | No       | URL of the article to generate topics from. Default is a sample url. |


#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  
  ```json
  {
    "topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
  }

### Endpoint: Generate article

#### URL

`GET /article/generate`

#### Method
- **GET**: *temporary*
- **POST**

#### Description
Generates an article, perex and 3 (*can be adjusted*) headline based on a given URL and topic using the LiteLLM service.

#### Parameters

##### Query Parameters

| Parameter | Type   | Required | Description                                                      |
|-----------|--------|----------|------------------------------------------------------------------|
| `url`     | string | No       | URL of the article to generate topics from. Default is a sample url. |


#### Responses

##### Success Response
- **Code**: 200 OK
- **Content**:
  
  ```json
  {
    "headlines": ["Headline 1", "Headline 2", "Headline 3"],
    "perex": "Indtroductory text to article.",
    "article": "The article itself in one block of text. newlines are indicated with '\n'."
  }
  
