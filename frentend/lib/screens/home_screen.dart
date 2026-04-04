import 'package:flutter/material.dart';
import '../models/chat.dart';
import '../models/message.dart';
import '../widgets/sidebar.dart';
import '../widgets/message_bubble.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late ScrollController _scrollController;
  List<Chat> chats = [];
  Chat? currentChat;
  late TextEditingController controller;
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
    controller = TextEditingController();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    controller.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    Future.delayed(Duration(milliseconds: 50), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void createNewChat() {
    Chat newChat = Chat(
      id: DateTime.now().toString(),
      title: "New Chat",
      messages: [],
    );

    setState(() {
      chats.add(newChat);
      currentChat = newChat;
    });
  }

  void sendMessage() async {
    if (currentChat == null) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Please create a new chat first")));
      return;
    }

    String text = controller.text.trim();
    if (text.isEmpty) return;

    // Clear input immediately
    controller.clear();

    setState(() {
      currentChat!.messages.add(Message(text: text, isUser: true));

      // 🔥 SET TITLE FROM FIRST MESSAGE
      if (currentChat!.messages.length == 1) {
        currentChat!.title = text.length > 30
            ? text.substring(0, 30) + "..."
            : text;
      }

      isLoading = true;
    });

    _scrollToBottom();

    try {
      String response = await ApiService.sendMessage(text);

      setState(() {
        currentChat!.messages.add(Message(text: response, isUser: false));
        isLoading = false;
      });

      _scrollToBottom();
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error: $e")));
    }
  }

  void deleteChat(Chat chat) {
    setState(() {
      chats.remove(chat);

      if (currentChat == chat) {
        currentChat = chats.isNotEmpty ? chats.first : null;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Sidebar(
            chats: chats,
            currentChat: currentChat,
            onSelect: (chat) => setState(() => currentChat = chat),
            onDelete: deleteChat,
            onNewChat: createNewChat,
          ),

          Expanded(
            child: Column(
              children: [
                Expanded(
                  child: currentChat == null
                      ? Center(
                          child: Text(
                            "Start a new chat",
                            style: TextStyle(fontSize: 18, color: Colors.grey),
                          ),
                        )
                      : ListView.builder(
                          controller: _scrollController,
                          padding: EdgeInsets.all(12),
                          itemCount: currentChat!.messages.length,
                          itemBuilder: (context, index) {
                            return MessageBubble(
                              message: currentChat!.messages[index],
                            );
                          },
                        ),
                ),

                if (isLoading)
                  Padding(
                    padding: EdgeInsets.all(8),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        ),
                        SizedBox(width: 10),
                        Text("Thinking..."),
                      ],
                    ),
                  ),

                Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Color(0xFF212121),
                    border: Border(
                      top: BorderSide(color: Colors.grey.shade800, width: 1),
                    ),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: controller,
                          enabled: !isLoading,
                          decoration: InputDecoration(
                            hintText: isLoading
                                ? "AI is thinking..."
                                : "Ask anything...",
                            filled: true,
                            fillColor: Color(0xFF343541),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(24),
                              borderSide: BorderSide.none,
                            ),
                            contentPadding: EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 12,
                            ),
                          ),
                          onSubmitted: (value) => sendMessage(),
                        ),
                      ),
                      SizedBox(width: 8),
                      Container(
                        decoration: BoxDecoration(
                          color: Color(0xFF10A37F),
                          borderRadius: BorderRadius.circular(24),
                        ),
                        child: IconButton(
                          icon: isLoading
                              ? SizedBox(
                                  width: 24,
                                  height: 24,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                    valueColor: AlwaysStoppedAnimation(
                                      Colors.white,
                                    ),
                                  ),
                                )
                              : Icon(Icons.send),
                          color: Colors.white,
                          onPressed: isLoading ? null : sendMessage,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
