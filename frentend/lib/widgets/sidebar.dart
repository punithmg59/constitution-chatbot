import 'package:flutter/material.dart';
import '../models/chat.dart';

class Sidebar extends StatelessWidget {
  final List<Chat> chats;
  final Chat? currentChat;
  final Function(Chat) onSelect;
  final Function(Chat) onDelete;
  final VoidCallback onNewChat;

  const Sidebar({
    required this.chats,
    required this.currentChat,
    required this.onSelect,
    required this.onDelete,
    required this.onNewChat,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 260,
      color: Color(0xFF202123),
      child: Column(
        children: [
          SizedBox(height: 16),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 12),
            child: SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color(0xFF10A37F),
                  padding: EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                onPressed: onNewChat,
                icon: Icon(Icons.add),
                label: Text(
                  "New Chat",
                  style: TextStyle(fontWeight: FontWeight.w600),
                ),
              ),
            ),
          ),
          SizedBox(height: 16),
          Expanded(
            child: ListView(
              children: chats.map((chat) {
                bool isActive = chat == currentChat;

                return Container(
                  margin: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: isActive ? Color(0xFF343541) : Colors.transparent,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: ListTile(
                    title: Text(
                      chat.title,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        fontSize: 14,
                        color: isActive ? Colors.white : Colors.grey[300],
                      ),
                    ),
                    trailing: IconButton(
                      icon: Icon(Icons.delete, size: 18),
                      onPressed: () => onDelete(chat),
                    ),
                    onTap: () => onSelect(chat),
                    contentPadding: EdgeInsets.symmetric(horizontal: 12),
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
