class Queries:


    ONTOLOGY_FINAL_QUERY = """
        CALL n10s.onto.import.fetch($ontology_url, $file_type) 
        YIELD terminationStatus, triplesLoaded, extraInfo
        WITH terminationStatus, triplesLoaded, extraInfo, $ontology_type AS username_prefix, '_xy_' AS identifier
        CALL apoc.do.when(
            terminationStatus = 'KO', 
            'RETURN extraInfo AS errorMessage', 
            'WITH username_prefix, identifier
             MATCH (n)
             UNWIND labels(n) AS label
             WITH n, label, username_prefix, identifier  
             WHERE NOT ANY(prefixed_label IN labels(n) WHERE prefixed_label STARTS WITH identifier)
             CALL {
                 WITH n, label, username_prefix, identifier
                 CALL apoc.create.addLabels(n, [identifier + username_prefix + label]) YIELD node
                 RETURN node
             }
             WITH count(*) AS processedNodes
             RETURN "Ontology imported successfully" AS successMessage',
            {extraInfo: extraInfo, username_prefix: username_prefix, identifier: identifier}
        ) YIELD value
        RETURN value;
        """
