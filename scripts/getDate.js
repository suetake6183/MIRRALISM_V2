#!/usr/bin/env node

/**
 * MIRRALISM 時刻確認スクリプト
 * Always適用ルール用 - 軽量・高速
 * 作成日: 2025年06月05日
 */

function getCurrentTimeInfo() {
    const now = new Date();
    
    // JST（日本標準時）への変換
    const jstOffset = 9 * 60; // UTC+9の分数
    const jstTime = new Date(now.getTime() + (jstOffset * 60 * 1000));
    
    // フォーマット関数
    const formatJapanese = (date) => {
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const dayOfWeek = ['日', '月', '火', '水', '木', '金', '土'][date.getDay()];
        
        return `${year}年${month}月${day}日（${dayOfWeek}）${hour}時${minute}分`;
    };
    
    const formatISO = (date) => {
        return date.toISOString().slice(0, 10); // YYYY-MM-DD
    };
    
    return {
        current_jst: formatJapanese(jstTime),
        iso_date: formatISO(jstTime),
        timestamp: jstTime.toISOString(),
        day_of_week: ['日', '月', '火', '水', '木', '金', '土'][jstTime.getDay()]
    };
}

// 実行
const timeInfo = getCurrentTimeInfo();

console.log('=== MIRRALISM現在時刻確認 ===');
console.log(`現在時刻: ${timeInfo.current_jst}`);
console.log(`ISO日付: ${timeInfo.iso_date}`);
console.log(`曜日: ${timeInfo.day_of_week}曜日`);
console.log('========================');

// 環境変数として出力（必要に応じて）
process.env.MIRRALISM_CURRENT_DATE = timeInfo.iso_date;
process.env.MIRRALISM_CURRENT_TIME_JST = timeInfo.current_jst;

// 正常終了
process.exit(0); 