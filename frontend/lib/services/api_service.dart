import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';

  // Upload resume using bytes (for web)
  static Future<Map<String, dynamic>> uploadResumeBytes(
    List<int> bytes,
    String filename,
  ) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload_resume'),
      );

      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          bytes,
          filename: filename,
        ),
      );

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to upload resume: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error uploading resume: $e');
    }
  }

  // Upload resume using file path (for desktop/mobile)
  static Future<Map<String, dynamic>> uploadResumePath(
    String filePath,
    String filename,
  ) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload_resume'),
      );

      request.files.add(
        await http.MultipartFile.fromPath('file', filePath),
      );

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to upload resume: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error uploading resume: $e');
    }
  }

  // Process resume against job description
  static Future<Map<String, dynamic>> processResume(
    String resumeId,
    String jobDescription,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/process_resume'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'resume_id': resumeId,
          'job_description': jobDescription,
        }),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to process resume: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error processing resume: $e');
    }
  }

  // Get top candidates
  static Future<Map<String, dynamic>> getTopCandidates(
      [String jobDescription = '']) async {
    try {
      final uri = jobDescription.isEmpty
          ? Uri.parse('$baseUrl/top_candidates')
          : Uri.parse('$baseUrl/top_candidates')
              .replace(queryParameters: {'job_description': jobDescription});

      final response = await http.get(uri);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to get candidates: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error getting candidates: $e');
    }
  }

  // Get cluster visualization data
  static Future<Map<String, dynamic>> getClusters() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/clusters'));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to get clusters: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error getting clusters: $e');
    }
  }

  // Export CSV
  static Future<List<int>> exportCsv() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/export_csv'));

      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        throw Exception('Failed to export CSV: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error exporting CSV: $e');
    }
  }
}

