import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../services/api_service.dart';
import '../models/candidate.dart';

class VisualizationPage extends StatefulWidget {
  const VisualizationPage({super.key});

  @override
  State<VisualizationPage> createState() => VisualizationPageState();
}

class VisualizationPageState extends State<VisualizationPage> {
  ClusterData? _clusterData;
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    loadClusterData();
  }

  Future<void> loadClusterData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = await ApiService.getClusters();
      setState(() {
        _clusterData = ClusterData.fromJson(response);
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Error loading cluster data: $e';
        _isLoading = false;
      });
    }
  }

  List<Color> _getClusterColors(int clusterLabel) {
    final colors = [
      Colors.blue,
      Colors.green,
      Colors.orange,
      Colors.purple,
      Colors.red,
      Colors.teal,
      Colors.pink,
    ];
    return [colors[clusterLabel % colors.length]];
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
                'Cluster Visualization',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              IconButton(
                icon: const Icon(Icons.refresh),
                onPressed: loadClusterData,
                tooltip: 'Refresh',
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Text(
            '2D visualization of candidate embeddings using PCA',
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey,
            ),
          ),
          const SizedBox(height: 24),
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
                      onPressed: loadClusterData,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            )
          else if (_clusterData == null ||
              _clusterData!.coordinates.isEmpty)
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.scatter_plot_outlined,
                        size: 64, color: Colors.grey[300]),
                    const SizedBox(height: 16),
                    const Text(
                      'No cluster data available',
                      style: TextStyle(fontSize: 18, color: Colors.grey),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Process resumes first to generate clusters',
                      style: TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              ),
            )
          else
            Expanded(
              child: Card(
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: ScatterChart(
                    ScatterChartData(
                      scatterSpots: _clusterData!.coordinates
                          .asMap()
                          .entries
                          .map((entry) {
                        final index = entry.key;
                        final coord = entry.value;
                        final clusterLabel =
                            _clusterData!.clusterLabels[index];
                        return ScatterSpot(
                          coord[0],
                          coord[1],
                          color: _getClusterColors(clusterLabel)[0],
                          radius: 8,
                        );
                      }).toList(),
                      minX: _clusterData!.coordinates
                              .map((c) => c[0])
                              .reduce((a, b) => a < b ? a : b) -
                          0.5,
                      maxX: _clusterData!.coordinates
                              .map((c) => c[0])
                              .reduce((a, b) => a > b ? a : b) +
                          0.5,
                      minY: _clusterData!.coordinates
                              .map((c) => c[1])
                              .reduce((a, b) => a < b ? a : b) -
                          0.5,
                      maxY: _clusterData!.coordinates
                              .map((c) => c[1])
                              .reduce((a, b) => a > b ? a : b) +
                          0.5,
                      gridData: FlGridData(
                        show: true,
                        drawVerticalLine: true,
                        drawHorizontalLine: true,
                      ),
                      titlesData: FlTitlesData(
                        show: true,
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            reservedSize: 40,
                          ),
                          axisNameWidget: const Text('PC1'),
                        ),
                        leftTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            reservedSize: 40,
                          ),
                          axisNameWidget: const Text('PC2'),
                        ),
                        topTitles: const AxisTitles(
                          sideTitles: SideTitles(showTitles: false),
                        ),
                        rightTitles: const AxisTitles(
                          sideTitles: SideTitles(showTitles: false),
                        ),
                      ),
                      borderData: FlBorderData(
                        show: true,
                        border: Border.all(color: Colors.grey[300]!),
                      ),
                    ),
                    swapAnimationDuration: const Duration(milliseconds: 300),
                    swapAnimationCurve: Curves.easeInOut,
                  ),
                ),
              ),
            ),
          if (_clusterData != null && _clusterData!.coordinates.isNotEmpty) ...[
            const SizedBox(height: 24),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Cluster Legend',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 16,
                      runSpacing: 8,
                      children: _clusterData!.clusterLabels
                          .toSet()
                          .map((clusterLabel) {
                        return Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Container(
                              width: 20,
                              height: 20,
                              decoration: BoxDecoration(
                                color: _getClusterColors(clusterLabel)[0],
                                shape: BoxShape.circle,
                              ),
                            ),
                            const SizedBox(width: 8),
                            Text('Cluster $clusterLabel'),
                          ],
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'Total Candidates: ${_clusterData!.coordinates.length}',
                      style: const TextStyle(
                        fontSize: 14,
                        color: Colors.grey,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

