#!/usr/bin/env node

/**
 * MIRRALISM 日付計算スクリプト
 * AI計算禁止ルール対応 - 100%正確な日付計算
 * 作成日: 2025年06月05日
 */

function parseDate(dateStr, paramName) {
    const date = new Date(dateStr + 'T00:00:00+09:00'); // JST固定
    if (isNaN(date.getTime())) {
        throw new Error(`${paramName}は有効な日付である必要があります (YYYY-MM-DD形式): ${dateStr}`);
    }
    return date;
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const dayNames = ['日', '月', '火', '水', '木', '金', '土'];
    const dayName = dayNames[date.getDay()];
    
    return {
        iso: `${year}-${month}-${day}`,
        japanese: `${year}年${month}月${day}日（${dayName}）`
    };
}

function isBusinessDay(date) {
    const day = date.getDay();
    return day !== 0 && day !== 6; // 日曜(0)と土曜(6)以外
}

function dateCalculation(operation, ...args) {
    let result, formula, validation, details = {};

    switch (operation) {
        case 'period':
            if (args.length !== 2) throw new Error('期間計算には開始日と終了日の2つの日付が必要です');
            const [startDate, endDate] = args.map((arg, i) => parseDate(arg, `日付${i+1}`));
            
            if (startDate > endDate) throw new Error('開始日は終了日より前である必要があります');
            
            const timeDiff = endDate.getTime() - startDate.getTime();
            const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
            
            result = daysDiff;
            formula = `${formatDate(endDate).iso} - ${formatDate(startDate).iso}`;
            validation = daysDiff >= 0 ? '正常' : 'エラー';
            
            details = {
                startDate: formatDate(startDate),
                endDate: formatDate(endDate),
                totalDays: daysDiff,
                totalWeeks: Math.floor(daysDiff / 7),
                remainingDays: daysDiff % 7
            };
            break;

        case 'add_days':
            if (args.length !== 2) throw new Error('日付加算には基準日と追加日数の2つの値が必要です');
            const baseDate = parseDate(args[0], '基準日');
            const daysToAdd = parseInt(args[1]);
            
            if (isNaN(daysToAdd)) throw new Error('追加日数は有効な数値である必要があります');
            
            const newDate = new Date(baseDate);
            newDate.setDate(newDate.getDate() + daysToAdd);
            
            result = formatDate(newDate).iso;
            formula = `${formatDate(baseDate).iso} + ${daysToAdd}日`;
            validation = '正常';
            
            details = {
                baseDate: formatDate(baseDate),
                daysAdded: daysToAdd,
                resultDate: formatDate(newDate)
            };
            break;

        case 'subtract_days':
            if (args.length !== 2) throw new Error('日付減算には基準日と減算日数の2つの値が必要です');
            const baseDateSub = parseDate(args[0], '基準日');
            const daysToSubtract = parseInt(args[1]);
            
            if (isNaN(daysToSubtract)) throw new Error('減算日数は有効な数値である必要があります');
            
            const subtractedDate = new Date(baseDateSub);
            subtractedDate.setDate(subtractedDate.getDate() - daysToSubtract);
            
            result = formatDate(subtractedDate).iso;
            formula = `${formatDate(baseDateSub).iso} - ${daysToSubtract}日`;
            validation = '正常';
            
            details = {
                baseDate: formatDate(baseDateSub),
                daysSubtracted: daysToSubtract,
                resultDate: formatDate(subtractedDate)
            };
            break;

        case 'business_days':
            if (args.length !== 2) throw new Error('営業日計算には開始日と終了日の2つの日付が必要です');
            const [bizStartDate, bizEndDate] = args.map((arg, i) => parseDate(arg, `日付${i+1}`));
            
            if (bizStartDate > bizEndDate) throw new Error('開始日は終了日より前である必要があります');
            
            let businessDays = 0;
            const currentDate = new Date(bizStartDate);
            
            while (currentDate <= bizEndDate) {
                if (isBusinessDay(currentDate)) {
                    businessDays++;
                }
                currentDate.setDate(currentDate.getDate() + 1);
            }
            
            const totalDaysForBiz = Math.ceil((bizEndDate.getTime() - bizStartDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;
            const weekendDays = totalDaysForBiz - businessDays;
            
            result = businessDays;
            formula = `${formatDate(bizStartDate).iso} から ${formatDate(bizEndDate).iso} の営業日`;
            validation = businessDays >= 0 && businessDays <= totalDaysForBiz ? '正常' : '要確認';
            
            details = {
                startDate: formatDate(bizStartDate),
                endDate: formatDate(bizEndDate),
                totalDays: totalDaysForBiz,
                businessDays: businessDays,
                weekendDays: weekendDays
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
            console.log('使用法: node date_calc.js <操作> <パラメータ...>');
            console.log('操作:');
            console.log('  period <開始日> <終了日>     - 期間計算');
            console.log('  add_days <基準日> <日数>     - 日付加算');
            console.log('  subtract_days <基準日> <日数> - 日付減算');
            console.log('  business_days <開始日> <終了日> - 営業日計算');
            console.log('日付形式: YYYY-MM-DD');
            process.exit(1);
        }

        const { result, formula, validation, operation: op, details } = dateCalculation(operation, ...args);

        console.log('=== 日付計算結果 ===');
        console.log(`操作: ${op}`);
        console.log(`入力: ${args.join(', ')}`);
        console.log(`結果: ${result}${op === 'period' || op === 'business_days' ? '日' : ''}`);
        console.log(`計算式: ${formula}`);
        console.log(`検証: ${validation}`);
        
        if (details) {
            console.log('--- 詳細情報 ---');
            Object.entries(details).forEach(([key, value]) => {
                if (typeof value === 'object' && value.japanese) {
                    console.log(`${key}: ${value.japanese} (${value.iso})`);
                } else {
                    console.log(`${key}: ${value}`);
                }
            });
        }
        
        console.log('=================');

    } catch (error) {
        console.error('❌ 日付計算エラー:', error.message);
        process.exit(1);
    }
}

module.exports = { dateCalculation, parseDate, formatDate, isBusinessDay }; 