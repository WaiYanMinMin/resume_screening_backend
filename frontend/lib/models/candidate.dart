class Candidate {
  final String resumeId;
  final String filename;
  final double similarityScore;
  final List<String> skills;
  final int clusterLabel;

  Candidate({
    required this.resumeId,
    required this.filename,
    required this.similarityScore,
    required this.skills,
    required this.clusterLabel,
  });

  factory Candidate.fromJson(Map<String, dynamic> json) {
    return Candidate(
      resumeId: json['resume_id'] ?? '',
      filename: json['filename'] ?? '',
      similarityScore: (json['similarity_score'] ?? 0.0).toDouble(),
      skills: json['skills'] != null
          ? List<String>.from(json['skills'])
          : [],
      clusterLabel: json['cluster_label'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'resume_id': resumeId,
      'filename': filename,
      'similarity_score': similarityScore,
      'skills': skills,
      'cluster_label': clusterLabel,
    };
  }
}

class ClusterData {
  final List<List<double>> coordinates;
  final List<int> clusterLabels;
  final List<String> resumeIds;

  ClusterData({
    required this.coordinates,
    required this.clusterLabels,
    required this.resumeIds,
  });

  factory ClusterData.fromJson(Map<String, dynamic> json) {
    return ClusterData(
      coordinates: json['coordinates'] != null
          ? (json['coordinates'] as List)
              .map((e) => List<double>.from(e))
              .toList()
          : [],
      clusterLabels: json['cluster_labels'] != null
          ? List<int>.from(json['cluster_labels'])
          : [],
      resumeIds: json['resume_ids'] != null
          ? List<String>.from(json['resume_ids'])
          : [],
    );
  }
}

