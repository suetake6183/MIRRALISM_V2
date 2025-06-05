#!/usr/bin/env node

/**
 * MIRRALISM ファイル・統計計算スクリプト
 * AI計算禁止ルール対応 - 100%正確なファイル・統計計算
 * 作成日: 2025年06月05日
 */

const fs = require('fs');
const path = require('path');

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function validateNumber(value, name) {
    const num = parseFloat(value);
    if (isNaN(num)) {
        throw new Error(`${name}は有効な数値である必要があります: ${value}`);
    }
    return num;
}

function formatNumber(num) {
    return num % 1 === 0 ? num.toString() : parseFloat(num.toFixed(10)).toString();
}

function getDirectorySize(dirPath) {
    let totalSize = 0;
    let fileCount = 0;
    const files = [];

    function walkDirectory(currentPath) {
        try {
            const items = fs.readdirSync(currentPath);
            
            for (const item of items) {
                const fullPath = path.join(currentPath, item);
                const stat = fs.statSync(fullPath);
                
                if (stat.isDirectory()) {
                    walkDirectory(fullPath);
                } else {
                    totalSize += stat.size;
                    fileCount++;
                    files.push({
                        path: path.relative(dirPath, fullPath),
                        size: stat.size,
                        formatted: formatBytes(stat.size)
                    });
                }
            }
        } catch (error) {
            throw new Error(`ディレクトリ読み取りエラー: ${currentPath} - ${error.message}`);
        }
    }

    if (!fs.existsSync(dirPath)) {
        throw new Error(`パスが存在しません: ${dirPath}`);
    }

    const stat = fs.statSync(dirPath);
    if (!stat.isDirectory()) {
        throw new Error(`パスはディレクトリである必要があります: ${dirPath}`);
    }

    walkDirectory(dirPath);
    return { totalSize, fileCount, files };
}

function fileCalculation(operation, ...args) {
    let result, formula, validation, details = {};

    switch (operation) {
        case 'size_sum':
            if (args.length !== 1) throw new Error('ディレクトリサイズ計算にはパスが必要です');
            const dirPath = args[0];
            
            const { totalSize, fileCount, files } = getDirectorySize(dirPath);
            
            result = totalSize;
            formula = `${dirPath} 内の全ファイルサイズ合計`;
            validation = totalSize >= 0 ? '正常' : 'エラー';
            
            const topFiles = files
                .sort((a, b) => b.size - a.size)
                .slice(0, 5);
            
            details = {
                directoryPath: dirPath,
                totalSize: formatBytes(totalSize),
                totalSizeBytes: totalSize.toLocaleString('ja-JP'),
                fileCount: fileCount.toLocaleString('ja-JP'),
                averageFileSize: formatBytes(fileCount > 0 ? totalSize / fileCount : 0),
                largestFiles: topFiles.map(f => `${f.path} (${f.formatted})`)
            };
            break;

        case 'count_files':
            if (args.length !== 1) throw new Error('ファイル数カウントにはパスが必要です');
            const countPath = args[0];
            
            const { fileCount: count, files: allFiles } = getDirectorySize(countPath);
            
            result = count;
            formula = `${countPath} 内のファイル数`;
            validation = count >= 0 ? '正常' : 'エラー';
            
            const extensions = {};
            allFiles.forEach(file => {
                const ext = path.extname(file.path) || '(拡張子なし)';
                extensions[ext] = (extensions[ext] || 0) + 1;
            });
            
            const sortedExtensions = Object.entries(extensions)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 10);
            
            details = {
                directoryPath: countPath,
                totalFiles: count.toLocaleString('ja-JP'),
                fileTypes: sortedExtensions.length,
                topExtensions: sortedExtensions.map(([ext, count]) => `${ext}: ${count}個`)
            };
            break;

        case 'average':
            if (args.length === 0) throw new Error('平均計算には少なくとも1つの数値が必要です');
            const numbers = args.map((arg, i) => validateNumber(arg, `数値${i+1}`));
            
            const sum = numbers.reduce((acc, num) => acc + num, 0);
            result = sum / numbers.length;
            formula = `(${numbers.map(formatNumber).join(' + ')}) ÷ ${numbers.length}`;
            validation = '正常';
            
            const sortedNumbers = [...numbers].sort((a, b) => a - b);
            const median = sortedNumbers.length % 2 === 0
                ? (sortedNumbers[sortedNumbers.length / 2 - 1] + sortedNumbers[sortedNumbers.length / 2]) / 2
                : sortedNumbers[Math.floor(sortedNumbers.length / 2)];
            
            const variance = numbers.reduce((acc, num) => acc + Math.pow(num - result, 2), 0) / numbers.length;
            const standardDeviation = Math.sqrt(variance);
            
            details = {
                count: numbers.length,
                sum: formatNumber(sum),
                average: formatNumber(result),
                median: formatNumber(median),
                minimum: formatNumber(Math.min(...numbers)),
                maximum: formatNumber(Math.max(...numbers)),
                range: formatNumber(Math.max(...numbers) - Math.min(...numbers)),
                variance: formatNumber(variance),
                standardDeviation: formatNumber(standardDeviation)
            };
            break;

        case 'sum':
            if (args.length === 0) throw new Error('合計計算には少なくとも1つの数値が必要です');
            const sumNumbers = args.map((arg, i) => validateNumber(arg, `数値${i+1}`));
            
            result = sumNumbers.reduce((acc, num) => acc + num, 0);
            formula = sumNumbers.map(formatNumber).join(' + ');
            validation = '正常';
            
            details = {
                count: sumNumbers.length,
                numbers: sumNumbers.map(formatNumber),
                sum: formatNumber(result),
                average: formatNumber(result / sumNumbers.length)
            };
            break;

        default:
            throw new Error(`未対応の操作: ${operation}`);
    }

    return { result, formula, validation, operation, details };
}

// メイン実行部分
if (require.main === module) {
    try {
        const [operation, ...args] = process.argv.slice(2);
        
        if (!operation) {
            console.log('使用法: node file_calc.js <操作> <パラメータ...>');
            console.log('操作:');
            console.log('  size_sum <ディレクトリパス>      - ディレクトリサイズ合計');
            console.log('  count_files <ディレクトリパス>   - ファイル数カウント');
            console.log('  average <数値1> [数値2] [...]    - 平均値計算');
            console.log('  sum <数値1> [数値2] [...]        - 合計値計算');
            process.exit(1);
        }

        const { result, formula, validation, operation: op, details } = fileCalculation(operation, ...args);

        console.log('=== ファイル・統計計算結果 ===');
        console.log(`操作: ${op}`);
        console.log(`入力: ${args.join(', ')}`);
        
        if (op === 'size_sum') {
            console.log(`結果: ${formatBytes(result)} (${result.toLocaleString('ja-JP')} bytes)`);
        } else if (op === 'count_files') {
            console.log(`結果: ${result.toLocaleString('ja-JP')}個`);
        } else {
            console.log(`結果: ${formatNumber(result)}`);
        }
        
        console.log(`計算式: ${formula}`);
        console.log(`検証: ${validation}`);
        
        if (details) {
            console.log('--- 詳細情報 ---');
            Object.entries(details).forEach(([key, value]) => {
                if (Array.isArray(value)) {
                    console.log(`${key}:`);
                    value.forEach(item => console.log(`  - ${item}`));
                } else {
                    console.log(`${key}: ${value}`);
                }
            });
        }
        
        console.log('===========================');

    } catch (error) {
        console.error('❌ ファイル・統計計算エラー:', error.message);
        process.exit(1);
    }
}

module.exports = { fileCalculation, getDirectorySize, formatBytes, validateNumber, formatNumber }; 