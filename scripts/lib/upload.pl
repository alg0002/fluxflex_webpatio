#┌─────────────────────────────────
#│ [ WebPatio ]
#│ upload.pl - 2007/06/30
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  アップロード
#-------------------------------------------------
sub upload {
	local($no) = @_;
	local(@ret);

	foreach $i (1 .. 3) {

		if (!defined($uplno{$i})) {
			push(@ret,("","",""));
			next;
		}

		local($w,$h);

		# Content-Typeヘッダからファイル種類を認識
		local($ex);
		if ($ctype{$i} =~ m|image/gif|i) {
			$ex = '.gif';
		} elsif ($ctype{$i} =~ m|image/p?jpeg|i) {
			$ex = '.jpg';
		} elsif ($ctype{$i} =~ m|image/png|i) {
			$ex = '.png';
		}

		# Content-Typeでは不明のときは拡張子からファイル種類を認識
		if (!$ex) {
			if ($fname{$i} =~ /\.gif$/) {
				$ex = '.gif';
			} elsif ($fname{$i} =~ /\.jpe?g$/) {
				$ex = '.jpg';
			} elsif ($fname{$i} =~ /\.png$/) {
				$ex = '.png';
			}
		}

		# ファイル認識できたときは書き込む
		if ($ex) {
			local($upfile) = $in{"upfile$i"};

			# マックバイナリ排除
			if ($macbin) {
				local($len) = substr($upfile, 83, 4);
				$len = unpack("%N", $len);
				$upfile = substr($upfile, 128, $len);
			}

			# アップファイル定義
			local($imgfile) = "$upldir/$no-$i$ex";

			# 書き込み
			open(OUT,">$imgfile") || &error("画像アップ失敗");
			binmode(OUT);
			print OUT $upfile;
			close(OUT);

			# パーミッション変更
			chmod(0666, $imgfile);

			# 画像サイズ取得
			if ($ex eq ".jpg") { ($w,$h) = &j_size($imgfile); }
			elsif ($ex eq ".gif") { ($w,$h) = &g_size($imgfile); }
			elsif ($ex eq ".png") { ($w,$h) = &p_size($imgfile); }
		}
		# 処理結果
		push(@ret,($ex,$w,$h));
	}
	# 返り値
	return @ret;
}

#-------------------------------------------------
#  JPEGサイズ認識
#-------------------------------------------------
sub j_size {
	local($jpeg) = @_;
	local($t, $m, $c, $l, $W, $H);

	open(JPEG, "$jpeg") || return (0,0);
	binmode JPEG;
	read(JPEG, $t, 2);
	while (1) {
		read(JPEG, $t, 4);
		($m, $c, $l) = unpack("a a n", $t);

		if ($m ne "\xFF") {
			$W = $H = 0;
			last;
		} elsif ((ord($c) >= 0xC0) && (ord($c) <= 0xC3)) {
			read(JPEG, $t, 5);
			($H, $W) = unpack("xnn", $t);
			last;
		} else {
			read(JPEG, $t, ($l - 2));
		}
	}
	close(JPEG);
	return ($W, $H);
}

#-------------------------------------------------
#  GIFサイズ認識
#-------------------------------------------------
sub g_size {
	local($gif) = @_;
	local($data);

	open(GIF,"$gif") || return (0,0);
	binmode(GIF);
	sysread(GIF,$data,10);
	close(GIF);

	if ($data =~ /^GIF/) { $data = substr($data,-4); }

	$W = unpack("v",substr($data,0,2));
	$H = unpack("v",substr($data,2,2));
	return ($W, $H);
}

#-------------------------------------------------
#  PNGサイズ認識
#-------------------------------------------------
sub p_size {
	local($png) = @_;
	local($data);

	open(PNG, "$png") || return (0,0);
	binmode(PNG);
	read(PNG, $data, 24);
	close(PNG);

	$W = unpack("N", substr($data, 16, 20));
	$H = unpack("N", substr($data, 20, 24));
	return ($W, $H);
}



1;

