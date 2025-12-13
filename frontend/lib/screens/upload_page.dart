import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../services/api_service.dart';

class UploadPage extends StatefulWidget {
  const UploadPage({super.key});

  @override
  State<UploadPage> createState() => _UploadPageState();
}

class _UploadPageState extends State<UploadPage> {
  bool _isUploading = false;
  String? _uploadMessage;
  bool _isSuccess = false;

  Future<void> _pickAndUploadFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf'],
        withData: kIsWeb, // Read bytes for web
      );

      if (result != null && result.files.single.name.isNotEmpty) {
        setState(() {
          _isUploading = true;
          _uploadMessage = null;
          _isSuccess = false;
        });

        final pickedFile = result.files.single;
        String filename = pickedFile.name;
        
        try {
          Map<String, dynamic> response;
          
          if (kIsWeb) {
            // Web: use bytes
            if (pickedFile.bytes == null) {
              throw Exception('Failed to read file bytes');
            }
            response = await ApiService.uploadResumeBytes(
              pickedFile.bytes!,
              filename,
            );
          } else {
            // Desktop/Mobile: use path
            if (pickedFile.path == null) {
              throw Exception('File path is not available');
            }
            response = await ApiService.uploadResumePath(
              pickedFile.path!,
              filename,
            );
          }
          
          setState(() {
            _isUploading = false;
            _uploadMessage = 'Successfully uploaded: ${response['filename']}\n'
                'Resume ID: ${response['resume_id']}';
            _isSuccess = true;
          });
        } catch (e) {
          setState(() {
            _isUploading = false;
            _uploadMessage = 'Error: $e';
            _isSuccess = false;
          });
        }
      }
    } catch (e) {
      setState(() {
        _isUploading = false;
        _uploadMessage = 'Error picking file: $e';
        _isSuccess = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Icon(
            Icons.upload_file,
            size: 80,
            color: Colors.blue[300],
          ),
          const SizedBox(height: 24),
          const Text(
            'Upload Resume',
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 16),
          const Text(
            'Select a PDF file to upload and process',
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
          ),
          const SizedBox(height: 32),
          ElevatedButton.icon(
            onPressed: _isUploading ? null : _pickAndUploadFile,
            icon: _isUploading
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.upload_file),
            label: Text(_isUploading ? 'Uploading...' : 'Select PDF File'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
          ),
          if (_uploadMessage != null) ...[
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: _isSuccess ? Colors.green[50] : Colors.red[50],
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: _isSuccess ? Colors.green : Colors.red,
                ),
              ),
              child: Text(
                _uploadMessage!,
                style: TextStyle(
                  color: _isSuccess ? Colors.green[900] : Colors.red[900],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

