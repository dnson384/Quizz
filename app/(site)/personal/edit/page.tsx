"use client";
import Image from "next/image";
import Header from "@/presentation/components/Layout/Header";
import SideMenu from "@/presentation/components/Layout/SideMenu";
import usePersonal from "@/presentation/hooks/Personal/usePersonal";
import HeaderAdmin from "@/presentation/components/Layout/Admin/HeaderAdmin";

export default function Personal() {
  const {
    error,
    user,
    newAvatar,
    fileInputRef,
    uploading,
    updateData,
    handleFileChange,
    handleButtonClick,
    handleFieldChange,
    handeSaveChangeClick,
    handleCancelChange,
  } = usePersonal();

  const currentName = updateData?.name !== null ? updateData?.name : user?.name;
  const currentEmail =
    updateData?.email !== null ? updateData?.email : user?.email;

  // 2. Validate trên giá trị thực tế này
  const isMissingName = !currentName || currentName.trim().length === 0;
  const isMissingEmail = !currentEmail || currentEmail.trim().length === 0;

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/g;
  const validPatternEmail = !!(currentEmail && emailRegex.test(currentEmail));

  const isValidForm: boolean =
    !isMissingName && !isMissingEmail && validPatternEmail;

  return (
    <>
      {user && (
        <>
          {user.role === "ADMIN" ? <HeaderAdmin /> : <Header />}
          <div className="mt-[74px]">
            <SideMenu />
            {error && (
              <div className="fixed inset-0 h-fit flex justify-center top-20">
                <div className="fixed z-10 h-fit inset-0 flex justify-center top-20">
                  <div className="flex items-center gap-2 bg-red-100 w-fit h-fit p-2 rounded-lg">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 512 512"
                    >
                      <path
                        fill="#f67c6f"
                        fillRule="evenodd"
                        d="M256 42.667c117.803 0 213.334 95.53 213.334 213.333S373.803 469.334 256 469.334S42.667 373.803 42.667 256S138.197 42.667 256 42.667m48.918 134.25L256 225.836l-48.917-48.917l-30.165 30.165L225.835 256l-48.917 48.918l30.165 30.165L256 286.166l48.918 48.917l30.165-30.165L286.166 256l48.917-48.917z"
                      />
                    </svg>
                    <p className=" text-red-400 select-none">{error}</p>
                  </div>
                </div>
              </div>
            )}

            <section className="w-6xl mx-auto flex flex-col gap-2">
              <div className="mb-5 flex items-center justify-between">
                <h3 className="text-2xl font-bold">Thông tin cá nhân</h3>
                <div className="flex gap-3">
                  <button
                    className="bg-gray-100 text-gray-500 font-bold py-2 px-5 rounded-full cursor-pointer hover:bg-gray-300"
                    onClick={handleCancelChange}
                  >
                    Huỷ
                  </button>
                  <button
                    className="bg-indigo-500 text-white font-bold py-2 px-5 rounded-full cursor-pointer hover:bg-indigo-700"
                    onClick={() => handeSaveChangeClick(isValidForm)}
                  >
                    Lưu
                  </button>
                </div>
              </div>

              {/* Ảnh đại diện */}
              <div className="px-6 py-4 border border-gray-300 rounded-xl">
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  className="hidden"
                  accept="image/*"
                />
                <div className="flex gap-10 items-center justify-between">
                  <div>
                    <h4 className="text-lg font-semibold mb-2">Ảnh hồ sơ</h4>
                    <Image
                      src={
                        newAvatar
                          ? `/api/images${newAvatar}`
                          : `/api/images${user.avatarUrl}`
                      }
                      alt={`avatar-${user.name}`}
                      width={100}
                      height={100}
                      className="w-[100px] h-[100px] rounded-full object-cover"
                    ></Image>
                  </div>

                  <button
                    className="px-4 py-2 bg-indigo-100 font-semibold rounded-xl shadow-md cursor-pointer hover:bg-indigo-500 hover:text-white"
                    onClick={handleButtonClick}
                    disabled={uploading}
                  >
                    Thay đổi ảnh hồ sơ
                  </button>
                </div>
              </div>

              {/* Tên người dùng */}
              <div className="px-6 py-4 border border-gray-300 rounded-xl">
                <div className="flex items-center justify-between">
                  <h4 className="text-lg font-semibold">Tên người dùng</h4>
                  <input
                    type="text"
                    name="name"
                    className={`w-xs px-2 py-1 border-b-2 text-end ${
                      isMissingName
                        ? "border-red-500 bg-red-50"
                        : "border-gray-300"
                    } focus:outline-0`}
                    required
                    placeholder="Tên người dùng mới"
                    defaultValue={user.name}
                    onChange={(e) => handleFieldChange(e)}
                  />
                </div>
              </div>

              {/* Email */}
              <div className="px-6 py-4 border border-gray-300 rounded-xl">
                <div className="flex items-center justify-between">
                  <h4 className="text-lg font-semibold">Email</h4>
                  <div className="flex flex-col items-end">
                    <input
                      type="email"
                      name="email"
                      className={`w-xs px-2 py-1 border-b-2 text-end ${
                        isMissingEmail || validPatternEmail === false
                          ? "border-red-500 bg-red-50"
                          : "border-gray-300"
                      } focus:outline-0`}
                      required
                      placeholder="Email người dùng mới"
                      defaultValue={user.email}
                      onBlur={(e) => handleFieldChange(e)}
                    />
                    {validPatternEmail === false && (
                      <span className="text-sm text-red-500">
                        Dữ liệu nhập không đúng định dạng
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Vai trò */}
              <div className="flex justify-between items-center px-6 py-4 border border-gray-300 rounded-xl">
                <h4 className="text-lg font-semibold">Loại tài khoản</h4>

                <div className="relative">
                  <select
                    name="role"
                    defaultValue={user.role}
                    className="appearance-none w-30 bg-indigo-50 border border-gray-200 px-4 py-2 rounded-md cursor-pointer focus:outline-none"
                    onBlur={(e) => handleFieldChange(e)}
                  >
                    {user.role === "ADMIN" && (
                      <option value="ADMIN">Admin</option>
                    )}
                    <option value="STUDENT">Học sinh</option>
                    <option value="TEACHER">Giáo viên</option>
                  </select>
                  <div className="absolute top-3 right-3">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill="none"
                        stroke="#374151"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="1.5"
                        d="m6 9l6 6l6-6"
                      />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Đổi mật khẩu */}
              {user.loginMethod === "EMAIL" ? (
                <button className="flex justify-between items-center px-6 py-4 border border-gray-300 rounded-xl cursor-pointer">
                  <h4 className="text-lg font-semibold">Đổi mật khẩu</h4>
                </button>
              ) : (
                <></>
              )}
            </section>
          </div>
        </>
      )}
    </>
  );
}
