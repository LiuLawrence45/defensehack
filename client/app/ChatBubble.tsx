// components/ChatBubble.js

export function ChatBubble({ message, senderName, senderImage, attachment }: any) {
    return (
        <div className="chat-bubble">
            <div className="sender-info">
                <img src={senderImage} alt={senderName} className="sender-image" />
                <span className="sender-name">{senderName}</span>
                <br />
                {attachment && (
                    <img src={attachment} alt="Attachment" className="w-1/2 mx-auto" />
                )}
            </div>
            <p className="message-text">{message}</p>
            <style jsx>{`
                .chat-bubble {
                    max-width: 80%;
                    padding: 20px;
                    margin: 5px 10px;
                    border-radius: 15px;
                    background-color: #e5e5ea;
                    color: black;
                    display: flex;
                    flex-direction: column;
                    align-items: flex-start;
                }
                .sender-info {
                    display: flex;
                    align-items: center;
                    margin-bottom: 15px;
                }
                .sender-image {
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin-right: 10px;
                }
                .sender-name {
                    font-size: 12px;
                    font-weight: bold;
                }
                .message-text {
                    font-size: 14px;
                    word-wrap: break-word;
                }
            `}</style>
        </div>
    );
}
