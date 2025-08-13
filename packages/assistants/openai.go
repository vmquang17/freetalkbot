package assistants

import (
	"fmt"
	"log/slog"
	"os"

	"github.com/felipem1210/freetalkbot/packages/common"
)

// Define a structure to match the JSON response
type OpenAI struct {
	Request   common.PostHttpReq
	Responses common.Responses
}

func (o OpenAI) sendPrompt() (common.Responses, error) {
	openaiResponses := o.Responses
	requestBody := o.Request.JsonBody
	slog.Debug(fmt.Sprintf("Message for openai: %v", requestBody["text"]), "jid", requestBody["sender"])
	o.Request.Url = os.Getenv("OPENAI_URL")
	body, err := o.Request.SendPost("json")
	if err != nil {
		return openaiResponses, fmt.Errorf("error sending message: %s", err)
	}

	openaiResponses, err = openaiResponses.ProcessJSONResponse(body)
	if err != nil {
		return openaiResponses, fmt.Errorf("error handling response body: %s", err)
	}
	return openaiResponses, nil
}

func (o OpenAI) Interact(sender string, message string) (common.Responses, error) {
	o.Request.JsonBody = map[string]string{"sender": sender, "text": message}
	responses, err := o.sendPrompt()
	if err != nil {
		return nil, err
	}
	return responses, nil
}
