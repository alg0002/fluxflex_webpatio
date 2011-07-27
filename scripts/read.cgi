#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ [ WebPatio ]
#│ patio.cgi - 2007/06/06
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

# 外部ファイル取り込み
require '../scripts/init.cgi';
require $jcode;

&parse_form;
&axscheck;
if ($mode eq "form") { &form; }
elsif ($mode eq "past") { &past; }
elsif ($mode eq "view2") { &view2; }
&view;

#-------------------------------------------------
#  スレッド閲覧
#-------------------------------------------------
sub view {
	local($no,$sub,$res,$key,$no2,$nam,$eml,$com,$dat,$ho,$pw,$url,$resub,$pno);
	local($job) = @_;

	# アラームを定義
	local($alarm) = int ($m_max * 0.9);

	# スマイルアイコン定義
	if ($smile) {
		@s1 = split(/\s+/, $smile1);
		@s2 = split(/\s+/, $smile2);
	}

	# 汚染チェック
	$in{'no'} =~ s/\D//g;

	# 過去ログ
	if ($job eq "past") {
		$bbsback = "mode=past";
		$guid = "<a href=\"$readcgi?mode=past\">過去ログ</a> &gt; 記事閲覧";

	# 現行ログ
	} else {
		# 参照数カウント
		local($data);
		open(DAT,"+< $logdir/$in{'no'}.dat") || &error("Open Error: $in{'no'}.dat");
		eval "flock(DAT, 2);";
		$data = <DAT>;

		# IP相違であれば更新
		($count,$ip) = split(/:/, $data);
		if ($addr ne $ip) {
			$count++;
			seek(DAT, 0, 0);
			print DAT "$count:$addr";
			truncate(DAT, tell(DAT));
		}
		close(DAT);

		$bbsback = "";
		$guid = "記事閲覧";
	}

	# スレッド読み込み
	open(IN,"$logdir/$in{'no'}.cgi") || &error("Open Error: $in{'no'}.cgi");
	$top1 = <IN>;
	$top2 = <IN>;
	chop($top2);

	($no,$sub,$res,$key) = split(/<>/, $top1);
	($no2,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/, $top2);
	$com = &auto_link($com, $no);
	$resub = "Re: $sub";
	$pno = $no;

	# アイコン定義
	if ($job ne "past" && $key eq '0') { $icon = 'fold3.gif'; }
	elsif ($job ne "past" && $key eq '2') { $icon = 'look.gif'; }
	elsif ($job ne "past" && $res >= $alarm) { $icon = 'fold5.gif'; }
	else { $icon = 'fold1.gif'; }

	# ヘッダ
	if ($job eq "past") {
		&header($sub);
	} else {
		&header($sub, "js");
		if ($key eq '0') {
			print "<table><tr><td width=\"5%\"></td>";
			print "<td width=\"95%\"><img src=\"$imgurl/alarm.gif\"> ";
			print "このスレッドは<b>ロック</b>されています。";
			print "記事の閲覧のみとなります。</td></tr></table>\n";

		} elsif ($key == 2) {
			print "<table><tr><td width=\"5%\"></td>";
			print "<td width=\"95%\"><img src=\"$imgurl/alarm.gif\"> ";
			print "このスレッドは<b>管理者からのメッセージ</b>です。";
			print "</td></tr></table>\n";

		} elsif ($alarm <= $res) {
			print "<table><tr><td width=\"5%\"></td>";
			print "<td width=\"95%\"><img src=\"$imgurl/alarm.gif\"> ";
			print "返信記事数が<b>$res</b>件あります。";
			print "<b>$m_max</b>件を超えると書き込みができなくなります。";
			print "</td></tr></table>\n";
		}
	}

	print <<"EOM";
<div align="center">
<table width="95%"><tr><td align="right" nowrap>
<a href="$bbscgi?">トップページ</a> &gt; $guid
</td></tr></table>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2"><td bgcolor="$col1">
<img src="$imgurl/$icon">
<font color="$col2"><b>$sub</b></font></td></tr>
<tr bgcolor="$col1"><td bgcolor="$col2" colspan=2>
<dl>
<dt>日時： $dat
<dt>名前： <b>$nam</b>
EOM

	if ($eml && $mvw ne '0') {
		print "&nbsp; &lt;<a href=\"mailto:$eml\" class=\"num\">$eml</a>&gt;\n";
	}
	if ($url) {
		print "<dt>参照： <a href=\"$url\" target=\"_blank\">$url</a>\n";
	}

	print "<br><br>\n<dd>$com\n";

	local($dd_flg);
	foreach $i (1 .. 3) {
		local($ex,$w,$h) = split(/,/, $upl{$i});
		next if (!$ex);

		if (!$dd_flg) {
			print "<dd>";
			$dd_flg++;
		}

		if (defined($imgex{$ex})) {
			local($w, $h) = &resize($w, $h);
			print "<a href=\"$uplurl/$tim-$i$ex\" target=\"_blank\">";
			print "<img src=\"$uplurl/$tim-$i$ex\" align=\"top\" border=\"0\" width=\"$w\" height=\"$h\" hspace=\"3\" vspace=\"5\"></a>\n";
		} else {
			print "[<a href=\"$uplurl/$tim-$i$ex\" target=\"_blank\">$tim-$i$ex</a>]\n";
		}
	}
	print "</dl>\n";

	# メンテボタン
	if ($job ne "past" && $key ne '2') {
		print "<div align=\"right\">";
		print "<a href=\"$registcgi?mode=mente&f=$in{'no'}\">";
		print "<img src=\"$imgurl/mente.gif\" alt=\"メンテ\" border=\"0\"></a></div>\n";
	}

	print <<EOM;
</td></tr></table>
</Td></Tr></Table>
<p>
EOM

	# ページ繰越ボタン
	local($pglog);
	if ($p eq "") { $p = 1; }
	if ($res > 0) {
		$end = $res / $t_max;
		if ($end != int($end)) { $end++; }
	} else {
		$end=1;
	}
	if ($key != 2) {
		$pglog = &pagelink($end, $p);
		print $pglog;
	}

	if ($res > 0) {
		print "<p><Table border=\"0\" cellspacing=\"0\" cellpadding=\"0\" width=\"95%\">";
		print "<Tr><Td bgcolor=\"$col1\">";
		print "<table border=\"0\" cellspacing=\"1\" cellpadding=\"5\" width=\"100%\">\n";
	}

	# 表示範囲を定義
	$from = $res - ($t_max * $p);
	$to   = $from + $t_max;

	$i = 0;
	while (<IN>) {
		$i++;
		if ($i <= $from) { next; }
		if ($i > $to) { last; }

		chop;
		($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw) = split(/<>/);
		$com = &auto_link($com, $in{'no'});

		print "<tr bgcolor=\"$col1\"><td bgcolor=\"$col3\" width=\"100%\">";
		print "<img src=\"$imgurl/file.gif\"> <b>$sub</b> ";
		print "<span class=\"num\">( No.$no )</span></td>";
		print "</tr><tr bgcolor=\"$col1\"><td bgcolor=\"$col2\">\n";
		print "<dl><dt>日時： $dat<dt>名前： <b>$nam</b>";

		if ($eml && $mvw ne '0') {
			print "&nbsp; &lt;<a href=\"mailto:$eml\" class=\"num\">$eml</a>&gt;";
		}
		if ($url) {
			print "<dt>参照： <a href=\"$url\" target=\"_blank\">$url</a>\n";
		}
		print "<br><br>\n<dd>$com</dl>\n";

		if ($job ne "past") {
			print "<div align=\"right\">";
			print "<a href=\"$registcgi?mode=mente&f=$in{'no'}&no=$no\">";
			print "<img src=\"$imgurl/mente.gif\" alt=\"メンテ\" border=\"0\"></a></div>";
		}
		print "</div></td></tr>\n";
	}
	close(IN);

	print "<tr><td><br></td></tr>" if (!$i);

	if ($res > 0) {
		print "</table></Td></Tr></Table><p>\n";
		print $pglog if ($pglog);
	}

	&form2 if ($job ne "past" && $key == 1);

	print "</div>\n</body></html>\n";
	exit;
}

#-------------------------------------------------
#  個別記事閲覧
#-------------------------------------------------
sub view2 {
	# スマイルアイコン定義
	if ($smile) {
		@s1 = split(/\s+/, $smile1);
		@s2 = split(/\s+/, $smile2);
	}

	# 汚染チェック
	$in{'f'}  =~ s/\D//g;

	# 記事No認識
	if ($in{'no'} =~ /^\d+$/) { $ptn = 1; $start = $in{'no'}; }
	elsif ($in{'no'} =~ /^(\d+)\-$/) { $ptn = 2; $start = $1; }
	elsif ($in{'no'} =~ /^(\d+)\-(\d+)$/) { $ptn = 3; $start = $1; $end = $2; }
	else { &error("記事Noが不正です"); }

	unless (-e "$logdir/$in{'f'}\.cgi") {
		 &error("スレッドが見当たりません");
	}

	&header($sub);
	print <<"EOM";
<div align="center">
<Table cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table cellspacing="1" cellpadding="5" width="100%">
EOM

	local($flag, $top);
	open(IN,"$logdir/$in{'f'}.cgi");
	$top = <IN>;
	while (<IN>) {
		local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw) = split(/<>/);
		if ($start == $no) { $flag=1; }
		if (!$flag) { next; }

		# 記事表示
		print "<tr bgcolor=\"$col1\"><td bgcolor=\"$col3\" width=\"100%\">";
		print "<img src=\"$imgurl/file.gif\"> <b>$sub</b> ";
		print "<span class=num>( No.$no )</span></td></tr>\n";
		print "<tr bgcolor=\"$col1\"><td bgcolor=\"$col2\">";
		print "<dl><dt>日時： $dat<dt>名前： <b>$nam</b>";

		if ($eml && $mvw ne '0') {
			print "&nbsp; &lt;<a href=\"mailto:$eml\" class=\"num\">$eml</a>&gt;\n";
		}
		if ($url) {
			print "<dt>参照： <a href=\"$url\" target=\"_blank\">$url</a>\n";
		}
		$com = &auto_link($com, $in{'f'});

		print "<br><br><dd>$com</dl><br></td></tr>\n";

		if (($ptn == 3 && $end == $no) || ($flag && $ptn == 1)) { last; }
	}
	close(IN);

	if (!$flag) {
		print "<tr bgcolor=\"$col1\"><th bgcolor=\"$col2\">";
		print "<h3>記事が見当たりません</h3></th></tr>\n";
	}

	print <<"EOM";
</table></Td></Tr></Table>
<br><br>
<form>
<input type="button" value="ウインドウを閉じる" onclick="top.close();">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  新規フォーム
#-------------------------------------------------
sub form {
	# 権限チェック
	if ($authkey && $my_rank < 2) {
		&error("投稿の権限がありません");
	}

	# ヘッダ
	if ($smile) { &header("", "js"); }
	else { &header(); }

	print <<"EOM";
<div align="center">
<table width="95%">
<tr>
  <td align="right" nowrap>
	<a href="$bbscgi?">トップページ</a> &gt; 新規スレッド作成
  </td>
</tr></table>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/pen.gif" align="middle">
&nbsp; <b>新規スレッド作成フォーム</b></td>
</tr></table></Td></Tr></Table>
EOM

	&form2("new");

	print "</div></body></html>\n";
	exit;
}

#-------------------------------------------------
#  フォーム内容
#-------------------------------------------------
sub form2 {
	local($job) = @_;
	local($submit);

	# 権限チェック
	if ($authkey && $my_rank < 2) {
		return;
	}

	# クッキー取得
	local($cnam,$ceml,$cpwd,$curl,$cmvw) = &get_cookie;
	if ($curl eq "") { $curl = "http://"; }

	if ($image_upl) {
		print qq|<form action="$registcgi" method="post" name="myFORM" enctype="multipart/form-data">\n|;
	} else {
		print qq|<form action="$registcgi" method="post" name="myFORM">\n|;
	}

	print <<EOM;
<input type="hidden" name="mode" value="regist">
<Table cellspacing="0" cellpadding="0" width="95%" border="0">
<Tr><Td bgcolor="$col1">
<table cellspacing="1" cellpadding="5" width="100%" border="0">
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">題名</th>
  <td><input type="text" name="sub" size="30" value="$resub" maxlength="30">
EOM

	if ($job eq "new") {
		$submit = 'スレッドを生成';
	} else {
		$submit = ' 返信する ';
		print "<input type=\"hidden\" name=\"res\" value=\"$in{'no'}\">\n";
		print "<input type=\"checkbox\" name=\"sort\" value=\"1\" checked>";
		print "スレッドをトップへソ\ート\n";
	}

	print <<"EOM";
  </td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">名前</th>
  <td><input type="text" name="name" size="30" value="$cnam" maxlength="20"></td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">E-Mail</th>
  <td bgcolor="$col2"><input type="text" name="email" size="30" value="$ceml">
  <select name="mvw">
EOM

	if ($cmvw eq "") { $cmvw = 1; }
	@mvw = ('非表示','表示');
	foreach (0,1) {
		if ($cmvw == $_) {
			print "<option value=\"$_\" selected>$mvw[$_]\n";
		} else {
			print "<option value=\"$_\">$mvw[$_]\n";
		}
	}

	print <<EOM;
</select></td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">URL</th>
  <td bgcolor="$col2"><input type="text" name="url" size="45" value="$curl"></td>
</tr>
EOM

	# 新規スレは画像フォーム
	if ($image_upl && $job eq "new") {
		print "<tr bgcolor=\"$col2\">\n";
		print "<td bgcolor=\"$col2\" width=\"80\" align=\"center\">";
		print "<b>画像添付</b><br><span style=\"font-size:9px\">JPEG/GIF/PNG</span></td>";
		print "<td bgcolor=\"$col2\">\n";

		foreach $i (1 .. 3) {
			print "<input type=\"file\" name=\"upfile$i\" size=\"45\"><br>\n";
		}

		print "</td></tr>\n";
	}

	print <<EOM;
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">パスワード</th>
  <td bgcolor="$col2">
  <input type="password" name="pwd" size="8" value="$cpwd" maxlength="8">
   （記事メンテ時に使用）
  </td>
</tr>
EOM

	# 投稿キー
	if ($regist_key) {

		# キー生成
		require $regkeypl;
		local($str_plain,$str_crypt) = &pcp_makekey;

		# 入力フォーム
		print qq |<tr bgcolor="$col2"><th bgcolor="$col2" width="80">投稿キー</th>|;
		print qq |<td bgcolor="$col2"><input type="text" name="regikey" size="6" style="ime-mode:inactive">\n|;
		print qq |（投稿時 <img src="$registkeycgi?$str_crypt" align="absmiddle" alt="投稿キー"> を入力してください）</td></tr>\n|;
		print qq |<input type="hidden" name="str_crypt" value="$str_crypt">\n|;
	}

	print <<EOM;
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">コメント</th>
  <td bgcolor="$col2">
EOM

	# アイコン
	if ($smile) {
		@s1 = split(/\s+/, $smile1);
		@s2 = split(/\s+/, $smile2);
		foreach (0 .. $#s1) {
			print "<a href=\"javascript:MyFace('$s2[$_]')\">";
			print "<img src=\"$imgurl/$s1[$_]\" border=\"0\"></a>\n";
		}
		print "<br>\n";
	}

	print <<"EOM";
<textarea name="comment" cols="48" rows="6" wrap="soft"></textarea></td></tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2"><br></td>
  <td bgcolor="$col2">
    <input type="submit" value="$submit"> &nbsp;&nbsp;
    <input type="checkbox" name="cook" value="on" checked>クッキー保存</td>
  </form></tr></table>
</Td></Tr></Table>
EOM
}

#-------------------------------------------------
#  過去ログ閲覧
#-------------------------------------------------
sub past {
	# 記事閲覧
	if ($in{'no'}) { &view("past");	}

	&header();
	print <<"EOM";
<div align="center">
<table width="95%"><tr><td align="right" nowrap>
<a href="$bbscgi?">トップページ</a> &gt; 過去ログ
</td></tr></table>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/memo1.gif" align="middle">
&nbsp;<b>過去ログ</b></td>
</tr></table></Td></Tr></Table>
<P>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="16"><br></td>
  <td bgcolor="$col2" width="80%"><b>スレッド</b></td>
  <td bgcolor="$col2" nowrap><b>投稿者</b></td>
  <td bgcolor="$col2" nowrap><b>返信数</b></td>
  <td bgcolor="$col2" nowrap><b>最終更新</b></td>
</tr>
EOM

	# スレッド展開
	local($i) = 0;
	if ($p eq "") { $p = 0; }
	open(IN,"$pastfile") || &error("Open Error: $pastfile");
	while (<IN>) {
		$i++;
		next if ($i < $p + 1);
		next if ($i > $p + $menu2);

		local($no,$sub,$res,$name,$date) = split(/<>/);

		print "<tr bgcolor=\"$col2\"><td bgcolor=\"$col2\" width=\"16\">";
		print "<img src=\"$imgurl/fold1.gif\"></td>";
		print "<td bgcolor=\"$col2\" width=\"80%\">";
		print "<a href=\"$readcgi?mode=past&no=$no\">$sub</a></td>";
		print "<td bgcolor=\"$col2\" nowrap>$name</td>";
		print "<td bgcolor=\"$col2\" align=\"right\" nowrap class=\"num\">$res</td>";
		print "<td bgcolor=\"$col2\" nowrap class=\"s1\">$date</td></tr>\n";
	}
	close(IN);

	if (!$i) {
		print "<td bgcolor=\"$col2\"></td>";
		print "<td colspan=\"4\" bgcolor=\"$col2\">- 現在過去ログはありません -</td>\n";
	}

	print "</table></Td></Tr></Table>\n";

	# ページ移動ボタン表示
	if ($p - $menu2 >= 0 || $p + $menu2 < $i) {
		local($x,$y) = (1,0);
		print "<p><table width=\"95%\"><tr><td class=\"num\"> Page: ";
		while ($i > 0) {
			if ($p == $y) {
				print "<b style=\"color:$pglog_col\">$x</b> |\n";
			} else {
				print "<a href=\"$readcgi?mode=past&p=$y\">$x</a> |\n";
			}
			$x++;
			$y += $menu2;
			$i -= $menu2;
		}
		print "</td></tr></table>\n";
	}

	print "</div>\n</body></html>\n";
	exit;
}


#-------------------------------------------------
#  ページ繰越ボタン
#-------------------------------------------------
sub pagelink {
	local($end,$p) = @_;
	local($pglog);

	$pglog .= "<table width=\"95%\"><tr><td class=\"num\">Page: ";
	foreach (1 .. $end) {
		if ($p == $_) {
			$pglog .= "<b style=\"color:$pglog_col\">$_</b> |\n";
		} else {
			$pglog .= "<a href=\"$readcgi?mode=$mode&no=$pno&p=$_\">$_</a> |\n";
		}
	}
	$pglog .= "</td></tr></table>\n";
	$pglog;
}

#-------------------------------------------------
#  リンク処理
#-------------------------------------------------
sub auto_link {
	local($msg, $f) = @_;

	$msg =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target=\"_target\">$2<\/a>/g;
	$msg =~ s/&gt;&gt;(\d)([\d\-]*)/<a href=\"$readcgi?mode=view2&f=$f&no=$1$2\" target=\"_blank\">&gt;&gt;$1$2<\/a>/gi;

	# スマイル画像変換
	if ($smile) {
		local($tmp);
		foreach (0 .. $#s1) {
			$tmp = $s2[$_];
			$tmp =~ s/([\+\*\.\?\^\$\[\-\]\|\(\)\\])/\\$1/g;
			$msg =~ s/$tmp/ <img src=\"$imgurl\/$s1[$_]\">/g;
		}
	}
	$msg;
}

#-------------------------------------------------
#  画像リサイズ
#-------------------------------------------------
sub resize {
	local($w,$h) = @_;

	# 画像表示縮小
	if ($w > $img_max_w || $h > $img_max_h) {

		local($w2,$h2,$key);

		$w2 = $img_max_w / $w;
		$h2 = $img_max_h / $h;

		if ($w2 < $h2) { $key = $w2; }
		else { $key = $h2; }

		$w = int ($w * $key) || 1;
		$h = int ($h * $key) || 1;
	}
	return ($w,$h);
}

#-------------------------------------------------
#  クッキー取得
#-------------------------------------------------
sub get_cookie {
	# クッキーを取得
	local($cook) = $ENV{'HTTP_COOKIE'};

	# 該当IDを取り出す
	local(%cook);
	foreach ( split(/;/, $cook) ) {
		local($key, $val) = split(/=/);
		$key =~ s/\s//g;

		$cook{$key} = $val;
	}

	# データをURLデコードして復元
	local(@cook);
	foreach ( split(/<>/, $cook{'WEB_PATIO'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("H2", $1)/eg;

		push(@cook,$_);
	}
	return @cook;
}



1;

