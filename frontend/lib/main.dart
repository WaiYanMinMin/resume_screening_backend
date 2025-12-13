import 'package:flutter/material.dart';
import 'screens/upload_page.dart';
import 'screens/job_description_page.dart';
import 'screens/ranking_page.dart';
import 'screens/visualization_page.dart';

void main() {
  runApp(const ResumeScreeningApp());
}

class ResumeScreeningApp extends StatelessWidget {
  const ResumeScreeningApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Resume Screening',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 2,
        ),
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _currentIndex = 0;
  final GlobalKey<RankingPageState> _rankingKey = GlobalKey<RankingPageState>();
  final GlobalKey<VisualizationPageState> _visualizationKey = GlobalKey<VisualizationPageState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resume Screening'),
      ),
      body: IndexedStack(
        index: _currentIndex,
        children: [
          const UploadPage(),
          const JobDescriptionPage(),
          RankingPage(key: _rankingKey),
          VisualizationPage(key: _visualizationKey),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
          // Refresh ranking page when navigating to it
          if (index == 2 && _rankingKey.currentState != null) {
            _rankingKey.currentState!.loadCandidates();
          }
          // Refresh visualization page when navigating to it
          if (index == 3 && _visualizationKey.currentState != null) {
            _visualizationKey.currentState!.loadClusterData();
          }
        },
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.upload_file),
            label: 'Upload',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.description),
            label: 'Job Description',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.leaderboard),
            label: 'Ranking',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.scatter_plot),
            label: 'Clusters',
          ),
        ],
      ),
    );
  }
}

