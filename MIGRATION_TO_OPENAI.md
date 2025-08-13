# Migration Guide: From Anthropic to OpenAI GPT-4o

This guide explains how to migrate from Anthropic Claude to OpenAI GPT-4o in FreeTalkBot.

## Changes Made

### 1. New OpenAI Assistant Service
- Created `assistants/openai/` directory with OpenAI GPT-4o integration
- Replaced Anthropic API calls with OpenAI API calls
- Converted function calling from Anthropic format to OpenAI format
- Maintained all existing tools (web_search, customer_info)

### 2. Updated Go Backend
- Added `packages/assistants/openai.go` handler
- Updated `packages/assistants/main.go` to support "openai" option
- Maintained existing interface compatibility

### 3. Configuration Changes
- Updated `.env.example` with OpenAI variables:
  - `ASSISTANT_TOOL=openai`
  - `STT_TOOL=whisper` (OpenAI Whisper API only)
  - `OPENAI_URL=http://openai:8088/chat`
  - `OPENAI_API_KEY=your-openai-api-key`
  - `OPENAI_MODEL=gpt-4o`

### 4. Docker Updates
- Replaced `anthropic` service with `openai` service
- Removed `whisper_cpu` service (no longer needed)
- Removed `hugging_face_cache` volume

### 5. STT Changes
- Now uses only OpenAI Whisper API (no local whisper server)
- Removed dependency on self-hosted whisper service

## Migration Steps

1. **Update Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and other settings
   ```

2. **Set Required Variables**:
   ```
   ASSISTANT_TOOL=openai
   STT_TOOL=whisper
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_MODEL=gpt-4o
   OPENAI_URL=http://openai:8088/chat
   OPENAI_TOKEN=your-openai-api-key
   ```

3. **Build and Run**:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

## Key Differences

### Anthropic vs OpenAI
- **Model**: Claude-3-Haiku → GPT-4o
- **API**: Anthropic API → OpenAI API
- **Function Calling**: Anthropic tools format → OpenAI functions format
- **Prompt Caching**: Removed (not available in OpenAI)

### Whisper Changes
- **Local Whisper**: Removed self-hosted whisper server
- **API Only**: Now uses OpenAI Whisper API exclusively
- **Simplified**: No need to manage whisper model downloads

## Verification

After migration, verify the system works by:

1. Check services are running:
   ```bash
   docker-compose ps
   ```

2. Test chat endpoint:
   ```bash
   curl -X POST http://localhost:8088/chat \
     -H "Content-Type: application/json" \
     -d '{"sender": "test", "text": "Hello"}'
   ```

3. Check logs:
   ```bash
   docker-compose logs openai
   ```

## Rollback

To rollback to Anthropic:
1. Set `ASSISTANT_TOOL=anthropic` in .env
2. Update docker-compose.yml to use anthropic service
3. Restart services

## Benefits of Migration

- **Latest Model**: GPT-4o provides state-of-the-art performance
- **Simplified Architecture**: No self-hosted whisper server needed
- **Better Integration**: Single OpenAI API for both chat and STT
- **Cost Efficiency**: OpenAI Whisper API is more cost-effective than self-hosting
- **Maintenance**: Reduced infrastructure complexity
