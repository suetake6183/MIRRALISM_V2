#!/usr/bin/env node

/**
 * MIRRALISM 基本数学計算スクリプト
 * AI計算禁止ルール対応 - 100%正確な計算
 * 作成日: 2025年06月05日
 */

function validateNumber(value, name) {
    const num = parseFloat(value);
    if (isNaN(num)) {
        throw new Error(`${name}は有効な数値である必要があります: ${value}`);
    }
    return num;
}

function formatNumber(num) {
    // 小数点以下が0の場合は整数表示、そうでなければ適切な桁数で表示
    return num % 1 === 0 ? num.toString() : parseFloat(num.toFixed(10)).toString();
}

function formatCurrency(num) {
    return num.toLocaleString('ja-JP');
}

function basicMath(operation, ...args) {
    let result, formula, validation;

    switch (operation) {
        case 'add':
            if (args.length < 2) throw new Error('加算には少なくとも2つの数値が必要です');
            const nums = args.map((arg, i) => validateNumber(arg, `数値${i+1}`));
            result = nums.reduce((sum, num) => sum + num, 0);
            formula = nums.join(' + ');
            validation = '正常';
            break;

        case 'subtract':
            if (args.length !== 2) throw new Error('減算には2つの数値が必要です');
            const [minuend, subtrahend] = args.map((arg, i) => validateNumber(arg, `数値${i+1}`));
            result = minuend - subtrahend;
            formula = `${formatNumber(minuend)} - ${formatNumber(subtrahend)}`;
            validation = '正常';
            break;

        case 'multiply':
            if (args.length < 2) throw new Error('乗算には少なくとも2つの数値が必要です');
            const factors = args.map((arg, i) => validateNumber(arg, `数値${i+1}`));
            result = factors.reduce((product, factor) => product * factor, 1);
            formula = factors.map(formatNumber).join(' × ');
            validation = '正常';
            break;

        case 'divide':
            if (args.length !== 2) throw new Error('除算には2つの数値が必要です');
            const [dividend, divisor] = args.map((arg, i) => validateNumber(arg, `数値${i+1}`));
            if (divisor === 0) throw new Error('0で割ることはできません');
            result = dividend / divisor;
            formula = `${formatNumber(dividend)} ÷ ${formatNumber(divisor)}`;
            validation = '正常';
            break;

        case 'percentage':
            if (args.length !== 2) throw new Error('パーセンテージ計算には2つの数値が必要です');
            const [numerator, denominator] = args.map((arg, i) => validateNumber(arg, `数値${i+1}`));
            if (denominator === 0) throw new Error('分母が0のパーセンテージは計算できません');
            result = (numerator / denominator) * 100;
            formula = `(${formatNumber(numerator)} ÷ ${formatNumber(denominator)}) × 100`;
            validation = result >= 0 && result <= 100000 ? '正常' : '要確認（通常範囲外）';
            break;

        case 'roi':
            if (args.length !== 2) throw new Error('ROI計算には投資額と回収額の2つの数値が必要です');
            const [investment, returns] = args.map((arg, i) => validateNumber(arg, i === 0 ? '投資額' : '回収額'));
            if (investment <= 0) throw new Error('投資額は正の数である必要があります');
            const profit = returns - investment;
            result = (profit / investment) * 100;
            formula = `((${formatNumber(returns)} - ${formatNumber(investment)}) ÷ ${formatNumber(investment)}) × 100`;
            validation = result > -100 ? '正常' : '要確認（100%以上の損失）';
            break;

        default:
            throw new Error(`未対応の操作: ${operation}`);
    }

    return { result, formula, validation, operation };
}

// メイン実行部分
if (require.main === module) {
    try {
        const [operation, ...args] = process.argv.slice(2);
        
        if (!operation) {
            console.log('使用法: node basic_math.js <操作> <数値1> [数値2] [...]');
            console.log('操作: add, subtract, multiply, divide, percentage, roi');
            process.exit(1);
        }

        const { result, formula, validation, operation: op } = basicMath(operation, ...args);

        console.log('=== 基本数学計算結果 ===');
        console.log(`操作: ${op}`);
        console.log(`入力: ${args.join(', ')}`);
        console.log(`結果: ${formatNumber(result)}${op === 'percentage' || op === 'roi' ? '%' : ''}`);
        console.log(`計算式: ${formula}${op === 'percentage' || op === 'roi' ? ' = ' + formatNumber(result) + '%' : ' = ' + formatNumber(result)}`);
        console.log(`検証: ${validation}`);
        
        if (op === 'roi') {
            const [investment, returns] = args.map(validateNumber);
            console.log(`詳細: 投資額 ${formatCurrency(investment)}円 → 回収額 ${formatCurrency(returns)}円`);
            console.log(`利益: ${formatCurrency(returns - investment)}円`);
        }
        
        console.log('======================');

    } catch (error) {
        console.error('❌ 計算エラー:', error.message);
        process.exit(1);
    }
}

module.exports = { basicMath, validateNumber, formatNumber }; 