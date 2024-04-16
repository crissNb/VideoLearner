# Video Learner

Knowledge Base AI from videos you provide

About
=====
Video Learner is designed to seamlessly integrate with your learning process. By providing input videos, Video Learner transcribes the content, transforming them into valuable resources. These transcriptions will then be used to answer any questions you might have!

How To Use
==========

### Requirements
- ffmpeg
- python

### Environment Variables
In order to use Video Learner, you need to set couple of environment variables. First, copy the `EnvironmentVariables.md` file to `.env`.
```bash
cp EnvironmentVariables.md .env
```

`API_Endpoint` is set to replace OpenAI API's embeddings. Run a text embeddings model using [open-text-embeddings](https://github.com/limcheekin/open-text-embeddings) and provide `API_Endpoint`.


### Prompt
To let Video Learner provide the best answer to you, it needs to have a good prompt. The prompt needs to be present in `prompt` file in the same directory (create one if it isn't there). Prompt should contain `{message}` and `{relevant_information}`, where `{message}` is your prompt to Video Learner and `{relevant_information}` is the information Video Learner fetches from its provided input videos.

### Input videos
Input videos must be stored in `input_videos` folder. Subdirectories are not allowed.

How It Works
============
Video Learner will first transform all the input videos into audio files, which will then be stored in `extracted_audio` folder. It then transcribes all those audio files to `learn_mats` folder. These transcriptions need to be then splitted into semantically valid chunks. The result of this process is stored in `learn_mats_chunked`.

When Video Learner is accessed with a prompt, it performs a similarity search in its database containing information from input videos. It then uses the result to provide the best answer.
