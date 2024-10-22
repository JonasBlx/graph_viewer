import React, { useState } from 'react';
import axios from 'axios';
import { ForceGraph3D } from 'react-force-graph';
import { TextField, Button } from '@mui/material';
import SpriteText from 'three-spritetext';

interface Node {
  id: number;
  name: string;
  color: string;
}

interface Link {
  source: number;
  target: number;
  weight: number;
}

interface Graph {
  name: string;
  nodes: Node[];
  links: Link[];
}

const App: React.FC = () => {
  const [numberOfNodes, setNumberOfNodes] = useState<number>(10);
  const [probability, setProbability] = useState<number>(0.5);
  const [graph, setGraph] = useState<Graph | null>(null);

  const generateGraph = async () => {
    try {
      const params = {
        number_of_nodes: numberOfNodes.toString(),
        probability_connection: probability.toString(),
      };
      console.log('Request params:', params);
      const response = await axios.get<Graph>('http://localhost:9191/random', {
        params: params,
      });
      console.log('Graph generated:', response.data);
      setGraph(response.data);
    } catch (error) {
      console.error('Error generating graph:', error);
    }
  };

  const colorGraph = async () => {
    if (!graph) return;
    try {
      const response = await axios.post<Graph>('http://localhost:9191/graph/color/dsatur', graph);
      setGraph(response.data);
    } catch (error) {
      console.error('Error coloring graph:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <TextField
          type="number"
          label="Number of Nodes"
          value={numberOfNodes}
          onChange={(e) => setNumberOfNodes(parseInt(e.target.value) || 0)}
          style={{ marginRight: '10px' }}
        />
        <TextField
          type="number"
          label="Probability of Connection"
          value={probability}
          onChange={(e) => {
            const value = parseFloat(e.target.value);
            setProbability(isNaN(value) ? 0 : value);
          }}
          style={{ marginRight: '10px' }}
        />
        <Button variant="contained" color="primary" onClick={generateGraph} style={{ marginRight: '10px' }}>
          Generate Graph
        </Button>
        <Button variant="contained" color="secondary" onClick={colorGraph} disabled={!graph}>
          Color Graph
        </Button>
      </div>
      {graph && (
        <ForceGraph3D
          graphData={{
            nodes: graph.nodes.map((node) => ({
              ...node,
              val: 1,
            })),
            links: graph.links,
          }}
          nodeAutoColorBy="color"
          nodeThreeObject={(node) => {
            const sprite = new SpriteText((node as Node).name);
            sprite.color = (node as Node).color;
            sprite.textHeight = 8;
            return sprite;
          }}
          linkDirectionalParticles={2}
          linkDirectionalParticleSpeed={0.005}
          width={window.innerWidth * 0.8}
          height={window.innerHeight * 0.6}
        />
      )}
    </div>
  );
};

export default App;
