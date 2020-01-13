port module Main exposing (main)

import Browser exposing (Document)
import Browser.Navigation as Nav
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Json.Encode exposing (Value, encode, object, string)


type ChatMessage
    = UserMessage String
    | BotMessage String
    | UploadedFile String


type alias Model =
    { messages : List ChatMessage
    , inputText : String
    }


init : Value -> ( Model, Cmd Msg )
init _ =
    ( { messages = []
      , inputText = ""
      }
    , Cmd.none
    )


view : Model -> Document Msg
view model =
    { title = "Chatbot"
    , body = [ showPage model ]
    }


showPage : Model -> Html Msg
showPage model =
    div [ class "main-container" ]
        [ div [ class "col-md-12" ]
            [ div [ class "panel panel-primary" ]
                [ div [ class "panel-heading" ]
                    [ span [ class "glyphicon glyphicon-comment" ] [] ]
                , div [ class "panel-body" ]
                    [ ul [ class "chat" ] <|
                        List.map
                            showMsg
                            model.messages
                    ]
                ]
            , div []
                [ textarea
                    [ style "width" "100%"
                    , onInput TypeMsg
                    ]
                    []
                , hr [] []
                , button [ onClick WsMsgSend ] [ text "Send Message" ]
                , hr [] []
                ]
            ]
        ]


showMsg : ChatMessage -> Html msg
showMsg message =
    case message of
        BotMessage msgText ->
            li [ class "left clearfix" ]
                [ div [ class "chat-body clearfix" ]
                    [ div [ class "header" ]
                        [ strong [ class "primary-font" ] [ text "Chatbot" ]
                        , small [ class "pull-right text-muted" ]
                            [ span [ class "glyphicon glyphicon-time" ] [] ]
                        ]
                    , p [] [ text msgText ]
                    ]
                ]

        UserMessage msgText ->
            li [ class "right clearfix" ]
                [ div [ class "chat-body clearfix" ]
                    [ div [ class "header" ]
                        [ small [ class "text-muted" ]
                            [ span [ class "glyphicon glyphicon-time" ] [] ]
                        , strong [ class "pull-right primary-font" ] [ text "You" ]
                        ]
                    , p [ class "pull-right" ] [ text msgText ]
                    ]
                ]

        UploadedFile filename ->
            li [ class "right clearfix" ]
                [ div [ class "chat-body clearfix" ]
                    [ div [ class "header" ]
                        [ small [ class "text-muted" ]
                            [ span [ class "glyphicon glyphicon-time" ] [] ]
                        , strong [ class "pull-right primary-font" ] [ text "You" ]
                        ]
                    , p [ class "pull-right" ]
                        [ span [ class "glyphicon glyphicon-file" ] []
                        , text filename
                        ]
                    ]
                ]


type Msg
    = TypeMsg String
    | WsMsgSend
    | WsMsgSendImg
    | WsMsgRecv String


port wsMsgSend : String -> Cmd msg


port wsMsgSendImg : ( String, String ) -> Cmd msg


port wsMsgRecv : (String -> msg) -> Sub msg


fileId : String
fileId =
    "file-upload-id"


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        TypeMsg text ->
            ( { model | inputText = text }, Cmd.none )

        WsMsgSend ->
            let
                message =
                    model.inputText
            in
            ( { model | messages = List.append model.messages [ UserMessage message ] }
            , wsMsgSend message
            )

        WsMsgSendImg ->
            let
                message =
                    model.inputText
            in
            ( { model | messages = List.append model.messages [ UserMessage message ] }, wsMsgSendImg ( fileId, message ) )

        WsMsgRecv message ->
            ( { model | messages = List.append model.messages [ BotMessage message ] }, Cmd.none )


subscription : Model -> Sub Msg
subscription model =
    wsMsgRecv WsMsgRecv


main : Program Value Model Msg
main =
    Browser.document
        { init = init
        , subscriptions = subscription
        , update = update
        , view = view
        }
