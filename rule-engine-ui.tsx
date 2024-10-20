import React, { useState } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';

const RuleEngine = () => {
  const [ruleString, setRuleString] = useState('');
  const [testData, setTestData] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleCreateRule = async () => {
    try {
      const response = await fetch('/api/rules/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule: ruleString }),
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail);
      
      setResult(data);
      setError('');
    } catch (err) {
      setError(err.message);
      setResult(null);
    }
  };

  const handleEvaluateRule = async () => {
    try {
      if (!result) throw new Error('Please create a rule first');
      
      const parsedData = JSON.parse(testData);
      const response = await fetch('/api/rules/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rule_ast: result,
          data: parsedData,
        }),
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail);
      
      setResult({ ...result, evaluation: data.result });
      setError('');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <Card className="mb-4">
        <CardHeader>Rule Engine</CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block mb-2">Rule String</label>
              <Input
                value={ruleString}
                onChange={(e) => setRuleString(e.target.value)}
                placeholder="Enter rule (e.g., age > 30 AND department = 'Sales')"
                className="w-full"
              />
            </div>
            
            <div>
              <label className="block mb-2">Test Data (JSON)</label>
              <Input
                value={testData}
                onChange={(e) => setTestData(e.target.value)}
                placeholder='{"age": 35, "department": "Sales"}'
                className="w-full"
              />
            </div>

            <div className="flex space-x-2">
              <Button onClick={handleCreateRule}>Create Rule</Button>
              <Button onClick={handleEvaluateRule}>Evaluate Rule</Button>
            </div>

            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {result && (
              <div className="mt-4">
                <h3 className="font-bold mb-2">Result:</h3>
                <pre className="bg-gray-100 p-4 rounded">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default RuleEngine;
