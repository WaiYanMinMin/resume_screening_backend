import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import '../services/api_service.dart';
import '../models/candidate.dart';

class RankingPage extends StatefulWidget {
  const RankingPage({super.key});

  @override
  State<RankingPage> createState() => RankingPageState();
}

class RankingPageState extends State<RankingPage> {

  List<Candidate> _candidates = [];
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    loadCandidates();
  }

  Future<void> loadCandidates() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = await ApiService.getTopCandidates();
      final candidatesJson = response['candidates'] as List?;
      
      if (candidatesJson != null) {
        setState(() {
          _candidates = candidatesJson
              .map((json) => Candidate.fromJson(json))
              .toList();
          _isLoading = false;
        });
      } else {
        setState(() {
          _candidates = [];
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Error loading candidates: $e';
        _isLoading = false;
      });
    }
  }

  Future<void> _exportCsv() async {
    try {
      final csvBytes = await ApiService.exportCsv();
      
      // Get downloads directory
      final directory = await getDownloadsDirectory();
      if (directory == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not access downloads directory')),
        );
        return;
      }

      final file = File('${directory.path}/ranked_candidates.csv');
      await file.writeAsBytes(csvBytes);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('CSV exported to ${file.path}'),
            duration: const Duration(seconds: 3),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error exporting CSV: $e')),
        );
      }
    }
  }

  Color _getScoreColor(double score) {
    if (score >= 0.7) return Colors.green;
    if (score >= 0.5) return Colors.orange;
    return Colors.red;
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Candidate Ranking',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Row(
                children: [
                  IconButton(
                    icon: const Icon(Icons.refresh),
                    onPressed: loadCandidates,
                    tooltip: 'Refresh',
                  ),
                  IconButton(
                    icon: const Icon(Icons.download),
                    onPressed: _candidates.isEmpty ? null : _exportCsv,
                    tooltip: 'Export CSV',
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 16),
          if (_isLoading)
            const Expanded(
              child: Center(child: CircularProgressIndicator()),
            )
          else if (_errorMessage != null)
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.error_outline, size: 64, color: Colors.red[300]),
                    const SizedBox(height: 16),
                    Text(
                      _errorMessage!,
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.red[700]),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: loadCandidates,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            )
          else if (_candidates.isEmpty)
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.inbox_outlined, size: 64, color: Colors.grey[300]),
                    const SizedBox(height: 16),
                    const Text(
                      'No candidates found',
                      style: TextStyle(fontSize: 18, color: Colors.grey),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Upload resumes and process them first',
                      style: TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              ),
            )
          else
            Expanded(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: SingleChildScrollView(
                  child: DataTable(
                    columns: const [
                      DataColumn(label: Text('Rank')),
                      DataColumn(label: Text('Filename')),
                      DataColumn(label: Text('Similarity Score')),
                      DataColumn(label: Text('Skills')),
                      DataColumn(label: Text('Cluster')),
                    ],
                    rows: _candidates.asMap().entries.map((entry) {
                      final index = entry.key;
                      final candidate = entry.value;
                      return DataRow(
                        cells: [
                          DataCell(Text('${index + 1}')),
                          DataCell(
                            SizedBox(
                              width: 150,
                              child: Text(
                                candidate.filename,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                          ),
                          DataCell(
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 8,
                                vertical: 4,
                              ),
                              decoration: BoxDecoration(
                                color: _getScoreColor(candidate.similarityScore)
                                    .withOpacity(0.2),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                (candidate.similarityScore * 100)
                                    .toStringAsFixed(1) +
                                    '%',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: _getScoreColor(candidate.similarityScore),
                                ),
                              ),
                            ),
                          ),
                          DataCell(
                            SizedBox(
                              width: 200,
                              child: Text(
                                candidate.skills.isEmpty
                                    ? 'N/A'
                                    : candidate.skills.join(', '),
                                overflow: TextOverflow.ellipsis,
                                maxLines: 2,
                              ),
                            ),
                          ),
                          DataCell(Text('${candidate.clusterLabel}')),
                        ],
                      );
                    }).toList(),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

