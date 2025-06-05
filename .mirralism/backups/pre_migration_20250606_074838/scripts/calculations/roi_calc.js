#!/usr/bin/env node

/**
 * MIRRALISM ROI・財務計算スクリプト
 * AI計算禁止ルール対応 - 100%正確な財務計算
 * 作成日: 2025年06月05日
 */

function validatePositiveNumber(value, name) {
    const num = parseFloat(value);
    if (isNaN(num) || num <= 0) {
        throw new Error(`${name}は正の数値である必要があります: ${value}`);
    }
    return num;
}

function validateNumber(value, name) {
    const num = parseFloat(value);
    if (isNaN(num)) {
        throw new Error(`${name}は有効な数値である必要があります: ${value}`);
    }
    return num;
}

function formatCurrency(num) {
    return num.toLocaleString('ja-JP');
}

function formatPercentage(num, decimals = 2) {
    return parseFloat(num.toFixed(decimals));
}

function roiCalculation(operation, ...args) {
    let result, formula, validation, details = {};

    switch (operation) {
        case 'roi':
            if (args.length !== 2) throw new Error('ROI計算には投資額と回収額の2つの数値が必要です');
            const [investment, returns] = args.map((arg, i) => 
                validatePositiveNumber(arg, i === 0 ? '投資額' : '回収額')
            );
            
            const profit = returns - investment;
            result = (profit / investment) * 100;
            formula = `((${formatCurrency(returns)} - ${formatCurrency(investment)}) ÷ ${formatCurrency(investment)}) × 100`;
            validation = result > -100 ? '正常' : '要確認（100%以上の損失）';
            
            details = {
                investment: `${formatCurrency(investment)}円`,
                returns: `${formatCurrency(returns)}円`,
                profit: `${formatCurrency(profit)}円`,
                profitStatus: profit >= 0 ? '利益' : '損失',
                roiCategory: result >= 100 ? '高ROI（2倍以上）' : 
                            result >= 50 ? '良好ROI（1.5倍以上）' : 
                            result >= 0 ? '正ROI（利益あり）' : '負ROI（損失）'
            };
            break;

        case 'profit_rate':
            if (args.length !== 2) throw new Error('利益率計算には利益額と売上額の2つの数値が必要です');
            const [profitAmount, revenue] = args.map((arg, i) => 
                validateNumber(arg, i === 0 ? '利益額' : '売上額')
            );
            
            if (revenue <= 0) throw new Error('売上額は正の数である必要があります');
            
            result = (profitAmount / revenue) * 100;
            formula = `(${formatCurrency(profitAmount)} ÷ ${formatCurrency(revenue)}) × 100`;
            validation = result >= -100 && result <= 100 ? '正常' : '要確認（異常値）';
            
            details = {
                profitAmount: `${formatCurrency(profitAmount)}円`,
                revenue: `${formatCurrency(revenue)}円`,
                cost: `${formatCurrency(revenue - profitAmount)}円`,
                profitMargin: result >= 20 ? '高利益率' : 
                             result >= 10 ? '標準利益率' : 
                             result >= 0 ? '低利益率' : '赤字'
            };
            break;

        case 'compound_growth':
            if (args.length !== 3) throw new Error('複利成長率計算には初期値、最終値、期間の3つの数値が必要です');
            const [initialValue, finalValue, periods] = args.map((arg, i) => {
                const names = ['初期値', '最終値', '期間'];
                return validatePositiveNumber(arg, names[i]);
            });
            
            if (periods < 1) throw new Error('期間は1以上である必要があります');
            
            result = (Math.pow(finalValue / initialValue, 1 / periods) - 1) * 100;
            formula = `((${formatCurrency(finalValue)} ÷ ${formatCurrency(initialValue)})^(1/${periods}) - 1) × 100`;
            validation = result > -50 && result < 1000 ? '正常' : '要確認（異常成長率）';
            
            const totalGrowth = ((finalValue - initialValue) / initialValue) * 100;
            
            details = {
                initialValue: `${formatCurrency(initialValue)}円`,
                finalValue: `${formatCurrency(finalValue)}円`,
                periods: `${periods}期間`,
                totalGrowth: `${formatPercentage(totalGrowth)}%`,
                annualGrowthRate: `${formatPercentage(result)}%`,
                growthCategory: result >= 20 ? '高成長' : 
                               result >= 10 ? '中成長' : 
                               result >= 0 ? '低成長' : 'マイナス成長'
            };
            break;

        case 'break_even':
            if (args.length !== 2) throw new Error('損益分岐点計算には固定費と単位利益の2つの数値が必要です');
            const [fixedCosts, unitProfit] = args.map((arg, i) => 
                validatePositiveNumber(arg, i === 0 ? '固定費' : '単位利益')
            );
            
            result = Math.ceil(fixedCosts / unitProfit);
            formula = `${formatCurrency(fixedCosts)} ÷ ${formatCurrency(unitProfit)}`;
            validation = result > 0 && result < 1000000 ? '正常' : '要確認';
            
            details = {
                fixedCosts: `${formatCurrency(fixedCosts)}円`,
                unitProfit: `${formatCurrency(unitProfit)}円`,
                breakEvenUnits: `${formatCurrency(result)}個`,
                breakEvenRevenue: `${formatCurrency(result * unitProfit)}円`,
                analysisNote: result <= 100 ? '達成容易' : 
                             result <= 1000 ? '要努力' : '困難'
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
            console.log('使用法: node roi_calc.js <操作> <パラメータ...>');
            console.log('操作:');
            console.log('  roi <投資額> <回収額>           - ROI計算');
            console.log('  profit_rate <利益額> <売上額>    - 利益率計算');
            console.log('  compound_growth <初期値> <最終値> <期間> - 複利成長率');
            console.log('  break_even <固定費> <単位利益>   - 損益分岐点');
            process.exit(1);
        }

        const { result, formula, validation, operation: op, details } = roiCalculation(operation, ...args);

        console.log('=== ROI・財務計算結果 ===');
        console.log(`操作: ${op}`);
        console.log(`入力: ${args.join(', ')}`);
        
        if (op === 'break_even') {
            console.log(`結果: ${formatCurrency(result)}個`);
        } else {
            console.log(`結果: ${formatPercentage(result)}%`);
        }
        
        console.log(`計算式: ${formula}`);
        console.log(`検証: ${validation}`);
        
        if (details) {
            console.log('--- 詳細分析 ---');
            Object.entries(details).forEach(([key, value]) => {
                console.log(`${key}: ${value}`);
            });
        }
        
        console.log('========================');

    } catch (error) {
        console.error('❌ ROI計算エラー:', error.message);
        process.exit(1);
    }
}

module.exports = { roiCalculation, validatePositiveNumber, validateNumber, formatCurrency, formatPercentage }; 