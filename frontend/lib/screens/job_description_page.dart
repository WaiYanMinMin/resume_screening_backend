import 'package:flutter/material.dart';
import '../services/api_service.dart';

class JobDescriptionPage extends StatefulWidget {
  const JobDescriptionPage({super.key});

  @override
  State<JobDescriptionPage> createState() => _JobDescriptionPageState();
}

class _JobDescriptionPageState extends State<JobDescriptionPage> {
  final TextEditingController _jobDescriptionController = TextEditingController();
  bool _isProcessing = false;
  String? _message;
  bool _isSuccess = false;

  // Store job description globally (in a real app, use a state management solution)
  static String? _storedJobDescription;

  static String? get storedJobDescription => _storedJobDescription;

  Future<void> _processAllResumes() async {
    final jobDescription = _jobDescriptionController.text.trim();
    
    if (jobDescription.isEmpty) {
      setState(() {
        _message = 'Please enter a job description';
        _isSuccess = false;
      });
      return;
    }

    setState(() {
      _isProcessing = true;
      _message = null;
      _isSuccess = false;
    });

    try {
      // Get all candidates and process them
      final response = await ApiService.getTopCandidates(jobDescription);
      
      // Store job description for later use
      _storedJobDescription = jobDescription;
      
      setState(() {
        _isProcessing = false;
        final count = response['candidates']?.length ?? 0;
        _message = 'Successfully processed $count candidates against job description';
        _isSuccess = true;
      });
    } catch (e) {
      setState(() {
        _isProcessing = false;
        _message = 'Error processing resumes: $e';
        _isSuccess = false;
      });
    }
  }

  @override
  void dispose() {
    _jobDescriptionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const SizedBox(height: 16),
          const Text(
            'Job Description',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'Enter the job description to match resumes against',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
          ),
          const SizedBox(height: 24),
          Expanded(
            child: TextField(
              controller: _jobDescriptionController,
              maxLines: null,
              expands: true,
              decoration: InputDecoration(
                hintText: 'Enter job description here...\n\nExample:\n'
                    'Software Engineer with experience in Python, FastAPI, and Machine Learning. '
                    'Should have knowledge of REST APIs, Docker, and cloud technologies.',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                filled: true,
                fillColor: Colors.grey[50],
              ),
            ),
          ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: _isProcessing ? null : _processAllResumes,
            icon: _isProcessing
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.search),
            label: Text(_isProcessing ? 'Processing...' : 'Process All Resumes'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
          ),
          if (_message != null) ...[
            const SizedBox(height: 16),
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
                _message!,
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

