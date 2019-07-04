<template>
	<div class="container">
		<h3>校對規則說明內容</h3>
		<p>雲端千眼校園版線上校對注意事項：</p>

		<ul style="list-style-type: cjk-ideographic;">
			<li>以段落為基準，每段即為一行，連續輸入不換行，直到該段落結束。辨識軟體基本上以這種方式輸出，如有遺漏請將分成多行的文字，但為同一段之內容，刪除其空格後合併成一行。</li>
			
			<div class="proofread_img">
				<img src="/static/ebookSystem/img/proofread_1.png" alt="校對規則說明，圖一">
			</div>

			<li>原則上每一段前面空兩格（半形）；章節為大標題者空四格(半形)，接下來的小標題空兩格(半形)。</li>
			<li>英文文句標點使用半形符號。</li>
			<li>中文文句標點使用全形符號，如遇到英文、數字仍使用半形符號。<br>
				（※ 全形與半形可利用SHIFT+空白鍵切換，或以滑鼠點擊切換。）
			</li>
			<li>當遇到特殊內容無法輸入、不知如何輸入時，請依種類插入相應標記。例如：圖片標記、數學標記、未知標記。</li>
			<li>如果遇到段落中有註釋，請將註釋標號註明於段落中並加上括號，例如：（註釋2），註釋內容則置於該段落之下一行，並於開頭標明前述之括號內容，無需空兩格。</li>
			<li>如遇有表格時，請使用校對編輯區中的表格工具。</li>
			<li>每一頁的頁首和頁尾如遇重覆性標題則捨棄不保留。</li>
			<li>遇到圖片時，可插入圖片標記，無須另外敘述圖片內容，如有圖說文字則可保留，例如：「圖7-2 PCR反應原理」。</li>
			<li>每頁之頁碼，請編輯於每頁第一個字之前，例如：（P.153）。</li>

			<div class="proofread_img">
				<img src="/static/ebookSystem/img/proofread_2.png" alt="校對規則說明，圖二">
			</div>
		</ul>
	</div>
</template>

<script>
	module.exports = {
		metaInfo: {
			title: '校園版校對規則',
		},
	}
</script>

<style>
p {
	font-size: 1.1rem;
}

ul > li {
	font-size: 1.1rem;
	padding-bottom: 0.4rem;
}

.proofread_img {
	margin: 1.5rem 0;
}

.proofread_img > img {
	width: 100%;
}

</style>
