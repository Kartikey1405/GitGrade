import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Folder, File, ChevronRight, ChevronDown } from 'lucide-react';

interface FileTreeProps {
  files: string[];
}

interface TreeNode {
  name: string;
  path: string;
  type: 'file' | 'folder';
  children?: TreeNode[];
}

const buildTree = (files: string[]): TreeNode[] => {
  const root: TreeNode[] = [];

  files.forEach((filePath) => {
    const parts = filePath.split('/').filter(Boolean);
    let currentLevel = root;

    parts.forEach((part, index) => {
      const isFile = index === parts.length - 1 && !filePath.endsWith('/');
      const existingNode = currentLevel.find((node) => node.name === part);

      if (existingNode) {
        currentLevel = existingNode.children || [];
      } else {
        const newNode: TreeNode = {
          name: part,
          path: parts.slice(0, index + 1).join('/'),
          type: isFile ? 'file' : 'folder',
          children: isFile ? undefined : [],
        };
        currentLevel.push(newNode);
        if (!isFile) {
          currentLevel = newNode.children!;
        }
      }
    });
  });

  return root;
};

const TreeItem = ({ node, depth = 0 }: { node: TreeNode; depth?: number }) => {
  const [isOpen, setIsOpen] = useState(depth < 2);
  const isFolder = node.type === 'folder';

  const getFileIcon = (name: string) => {
    const ext = name.split('.').pop()?.toLowerCase();
    const iconMap: Record<string, string> = {
      ts: '🔷',
      tsx: '⚛️',
      js: '🟨',
      jsx: '⚛️',
      py: '🐍',
      json: '📋',
      md: '📝',
      css: '🎨',
      html: '🌐',
      yml: '⚙️',
      yaml: '⚙️',
    };
    return iconMap[ext || ''] || '';
  };

  return (
    <div>
      <motion.div
        className={`flex items-center gap-2 py-1.5 px-2 rounded-lg cursor-pointer transition-colors
          ${isFolder ? 'hover:bg-neon/10' : 'hover:bg-muted/50'}`}
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
        onClick={() => isFolder && setIsOpen(!isOpen)}
        whileHover={{ x: 2 }}
      >
        {isFolder ? (
          <>
            <motion.div
              animate={{ rotate: isOpen ? 90 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChevronRight className="w-4 h-4 text-muted-foreground" />
            </motion.div>
            <Folder className={`w-4 h-4 ${isOpen ? 'text-neon' : 'text-neon/60'}`} />
          </>
        ) : (
          <>
            <span className="w-4" />
            <span className="text-sm">{getFileIcon(node.name)}</span>
            <File className="w-4 h-4 text-muted-foreground" />
          </>
        )}
        <span className={`text-sm ${isFolder ? 'font-medium text-foreground' : 'text-muted-foreground'}`}>
          {node.name}
        </span>
      </motion.div>

      <AnimatePresence>
        {isFolder && isOpen && node.children && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
          >
            {node.children
              .sort((a, b) => {
                if (a.type === b.type) return a.name.localeCompare(b.name);
                return a.type === 'folder' ? -1 : 1;
              })
              .map((child) => (
                <TreeItem key={child.path} node={child} depth={depth + 1} />
              ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const FileTree = ({ files }: FileTreeProps) => {
  const tree = buildTree(files);

  return (
    <div className="glass-card p-6 h-full overflow-hidden">
      <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
        <Folder className="w-5 h-5 text-neon" />
        File Structure
      </h3>
      <div className="overflow-auto max-h-[400px] pr-2 -mr-2">
        {tree.map((node) => (
          <TreeItem key={node.path} node={node} />
        ))}
      </div>
    </div>
  );
};

export default FileTree;
